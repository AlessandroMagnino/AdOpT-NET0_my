from pathlib import Path
import shutil
import time
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

import adopt_net0.data_preprocessing as dp
import adopt_net0.data_preprocessing.model_definition as model
from adopt_net0.modelhub import ModelHub

from setup_case_study import setup_brownfield, setup_emissions_limits


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)


def _copy_results_to_canonical_path(result_folder: Path, pathway: str, year: str):
    canonical_folder = Path("output") / pathway / year
    canonical_folder.mkdir(parents=True, exist_ok=True)

    source_file = result_folder / "optimization_results.h5"
    if not source_file.exists():
        raise FileNotFoundError(f"Expected results file not found: {source_file}")

    shutil.copy2(source_file, canonical_folder / "optimization_results.h5")


def run_path(pathway: str, year: str):
    """
    Run a single year of a pathway.
    Case study is the year.
    """
    input_path = Path("input") / pathway / year
    output_path = Path("output") / pathway

    dp.create_optimization_templates(str(input_path), str(output_path))

    model.topology_definition(f"{pathway}/{year}", str(input_path))

    dp.create_input_data_folder_template(str(input_path))

    model.nodes_location_definition(f"{pathway}/{year}", str(input_path))
    model.networks_definition(f"{pathway}/{year}", str(input_path))
    model.technologies_definition(f"{pathway}/{year}", str(input_path))

    dp.copy_technology_data(str(input_path))
    dp.copy_network_data(str(input_path))
    dp.copy_compressor_data(str(input_path))

    dp.fill_carrier_data(str(input_path), value_or_data=0)
    dp.fill_carrier_pressure_data(str(input_path), pressure_value_bar=0)

    model.carrier_data_definition(f"{pathway}/{year}", str(input_path))
    model.carbon_costs_definition(f"{pathway}/{year}", str(input_path))
    model.optimization_options_definition(f"{pathway}/{year}", str(input_path))

    pyhub = ModelHub()
    pyhub.read_data(str(input_path))

    start_time = time.time()

    pyhub.quick_solve(case_study=year)

    _copy_results_to_canonical_path(
        Path(pyhub.last_solve_info["result_folder_path"]),
        pathway,
        year,
    )

    elapsed = time.time() - start_time
    logging.info("Solved %s/%s in %.1f seconds", pathway, year, elapsed)

    return elapsed


def run_pathway_sequence(pathway: str, years: list[str], overwrite_first_year: bool = False):
    """
    Run one full pathway sequentially.

    Example:
        pathway/2020 -> pathway/2025 -> pathway/2030 -> pathway/2040 -> pathway/2050

    This function is intended to run inside one process.
    Different pathways can be run in parallel.
    """
    pathway_start = time.time()

    logging.info("Starting pathway: %s", pathway)

    yearly_results = []

    for index, year in enumerate(years):
        case_study_dir = Path("case_studies") / pathway / year

        if not case_study_dir.exists():
            raise ValueError(
                f"Year {year} does not exist in the pathway folder: {case_study_dir}"
            )

        if index > 0:
            logging.info("[%s] Setting up case study for %s", pathway, year)
            setup_brownfield(pathway, year)
            setup_emissions_limits(pathway, year)

        else:
            output_dir = Path("output") / pathway

            if output_dir.exists() and any(output_dir.iterdir()):
                if overwrite_first_year:
                    logging.warning(
                        "[%s] Output directory already exists and will be removed: %s",
                        pathway,
                        output_dir,
                    )
                    shutil.rmtree(output_dir)
                else:
                    raise FileExistsError(
                        f"Output directory already exists for the pathway: {output_dir}. "
                        "Please remove or rename it before running the first year, "
                        "or set OVERWRITE_FIRST_YEAR = True."
                    )

        logging.info("[%s] Running case study for %s", pathway, year)

        year_start = time.time()
        elapsed = run_path(pathway, year)
        year_total = time.time() - year_start

        yearly_results.append(
            {
                "pathway": pathway,
                "year": year,
                "success": True,
                "solve_elapsed": elapsed,
                "total_elapsed": year_total,
            }
        )

    pathway_elapsed = time.time() - pathway_start

    logging.info(
        "Completed pathway %s in %.1f seconds",
        pathway,
        pathway_elapsed,
    )

    return {
        "pathway": pathway,
        "success": True,
        "elapsed": pathway_elapsed,
        "years": yearly_results,
    }


def run_multiple_pathways(
    pathways: list[str],
    years: list[str],
    workers: int | None = None,
    overwrite_first_year: bool = False,
):
    if workers is None:
        workers = min(len(pathways), max(1, multiprocessing.cpu_count() // 8))

    logging.info("Pathways: %s", pathways)
    logging.info("Years: %s", years)
    logging.info("Workers: %d", workers)

    results = []

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                run_pathway_sequence,
                pathway,
                years,
                overwrite_first_year,
            ): pathway
            for pathway in pathways
        }

        for future in as_completed(futures):
            pathway = futures[future]

            try:
                result = future.result()
                results.append(result)

                if result.get("success"):
                    logging.info("Pathway completed successfully: %s", pathway)
                else:
                    logging.error("Pathway failed: %s", pathway)

            except Exception as exc:
                logging.exception(
                    "Unhandled error while running pathway %s",
                    pathway,
                )
                results.append(
                    {
                        "pathway": pathway,
                        "success": False,
                        "error": str(exc),
                    }
                )

    success_count = sum(1 for result in results if result.get("success"))

    logging.info(
        "Summary: %d/%d pathways completed successfully",
        success_count,
        len(pathways),
    )

    failed = [r for r in results if not r.get("success")]
    if failed:
        logging.error("Failed pathways:")
        for item in failed:
            logging.error(
                "  %s: %s",
                item.get("pathway"),
                item.get("error", "unknown error"),
            )

    return results


if __name__ == "__main__":

    PATHWAYS = [
        "base_case_90_5_dd",
        "base_case_80_5_dd",
        "base_case_70_5_dd",
        "base_case_60_5_dd",
        "base_case_50_5_dd",
        "base_case_00_5_dd"
    ]

    YEARS = ["2020", "2025", "2030", "2040", "2050"]

    WORKERS = 4

    # False = if output/pathway already exists and is not empty, stop.
    # True  = delete output/pathway before running the first year.
    OVERWRITE_FIRST_YEAR = False

    run_multiple_pathways(
        pathways=PATHWAYS,
        years=YEARS,
        workers=WORKERS,
        overwrite_first_year=OVERWRITE_FIRST_YEAR,
    )