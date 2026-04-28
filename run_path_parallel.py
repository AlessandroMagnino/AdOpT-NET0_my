from pathlib import Path
import shutil
import time
import argparse
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

import adopt_net0.data_preprocessing as dp
import adopt_net0.data_preprocessing.model_definition as model
from adopt_net0.modelhub import ModelHub

from setup_case_study import setup_brownfield, setup_emissions_limits

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def _copy_results_to_canonical_path(result_folder: Path, pathway: str, year: str):
    canonical_folder = Path("output") / pathway / year
    canonical_folder.mkdir(parents=True, exist_ok=True)

    source_file = result_folder / "optimization_results.h5"
    if not source_file.exists():
        raise FileNotFoundError(f"Expected results file not found: {source_file}")

    shutil.copy2(source_file, canonical_folder / "optimization_results.h5")


def run_case(pathway: str, year: str, do_setup: bool = False):
    """Run a single case (independent). If `do_setup` is True, runs brownfield/emissions setup prior to solving.

    Warning: running dependent years of the same pathway in parallel may break brownfield/setup expectations.
    Use parallel runs only for independent cases (different pathways or years without brownfield dependency).
    """
    try:
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

        _copy_results_to_canonical_path(Path(pyhub.last_solve_info["result_folder_path"]), pathway, year)

        end_time = time.time()
        elapsed = end_time - start_time
        logging.info(f"Solved {pathway}/{year} in {elapsed:.1f}s")
        return {"pathway": pathway, "year": year, "success": True, "elapsed": elapsed}

    except Exception as e:
        logging.exception("Error running case %s/%s", pathway, year)
        return {"pathway": pathway, "year": year, "success": False, "error": str(e)}


def parse_cases_arg(cases_arg: str):
    """Parse cases string like "base_case:2020,base_case:2025,other:2030" into list of (pathway, year)."""
    cases = []
    for token in cases_arg.split(','):
        token = token.strip()
        if not token:
            continue
        if ':' not in token:
            raise ValueError(f"Invalid case token: {token}. Expected format pathway:year")
        pathway, year = token.split(':', 1)
        cases.append((pathway, year))
    return cases


def main():
    parser = argparse.ArgumentParser(description="Run multiple independent case studies in parallel.")
    parser.add_argument('--cases', required=True, help="Comma-separated list of cases as pathway:year e.g. base_case:2020,base_case:2025")
    parser.add_argument('--workers', type=int, default=max(1, multiprocessing.cpu_count() - 1), help="Number of parallel workers")
    parser.add_argument('--skip-setup', action='store_true', help="Skip setup_brownfield/setup_emissions_limits. Use when cases are already prepared.")

    args = parser.parse_args()

    cases = parse_cases_arg(args.cases)

    # Safety note: if cases include multiple years of same pathway where brownfield setup is required,
    # parallel execution may produce incorrect results. The user should ensure cases are independent.
    pathways = set([p for p, y in cases])
    if len(cases) > 1:
        logging.info("Running %d cases across %d pathways with %d workers", len(cases), len(pathways), args.workers)

    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as exe:
        futures = {exe.submit(run_case, p, y, not args.skip_setup): (p, y) for p, y in cases}
        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)
            if res.get('success'):
                logging.info("Completed %s/%s", res['pathway'], res['year'])
            else:
                logging.error("Failed %s/%s: %s", res['pathway'], res['year'], res.get('error'))

    # Summary
    success_count = sum(1 for r in results if r.get('success'))
    logging.info("Summary: %d/%d succeeded", success_count, len(results))


if __name__ == '__main__':
    main()
