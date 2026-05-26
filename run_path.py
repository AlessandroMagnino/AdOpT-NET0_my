from pathlib import Path
import shutil
import time

import adopt_net0.data_preprocessing as dp
import adopt_net0.data_preprocessing.model_definition as model
from adopt_net0.modelhub import ModelHub

from setup_case_study import setup_brownfield, setup_emissions_limits

def _copy_results_to_canonical_path(result_folder: Path, pathway: str, year: str):
    canonical_folder = Path("output") / pathway / year
    canonical_folder.mkdir(parents=True, exist_ok=True)

    source_file = result_folder / "optimization_results.h5"
    if not source_file.exists():
        raise FileNotFoundError(f"Expected results file not found: {source_file}")

    shutil.copy2(source_file, canonical_folder / "optimization_results.h5")


def run_path(pathway: str, year: str):
    """
    Case study is the year
    """
    # Specify the path to your input data
    input_path = Path("input") / pathway / year
    output_path = Path("output") / pathway

    # Create template files (comment these lines if already defined)
    dp.create_optimization_templates(str(input_path), str(output_path))

    # Topology definition
    model.topology_definition(f"{pathway}/{year}", str(input_path))

    # Create folder structure (comment these lines if already defined)
    dp.create_input_data_folder_template(str(input_path))

    # Define nodes locations (comment these lines if already defined)
    model.nodes_location_definition(f"{pathway}/{year}", str(input_path))

    # Define networks (comment these lines if already defined)
    model.networks_definition(f"{pathway}/{year}", str(input_path))

    # Define technologies on each node (comment these lines if already defined)
    model.technologies_definition(f"{pathway}/{year}", str(input_path))

    # Copy technology and network data into folder (comment these lines if already defined)
    dp.copy_technology_data(str(input_path))
    dp.copy_network_data(str(input_path))
    dp.copy_compressor_data(str(input_path))

    # Correct data on technologies and networks if needed (comment these lines if already defined)
    # model.technologies_data_correction(input_path)

    # Correct data on networks if needed (comment these lines if already defined)
    # model.networks_data_correction(input_path)

    # Read climate data and fill carried data (comment these lines if already defined)
    # dp.load_climate_data_from_api(input_path)
    dp.fill_carrier_data(str(input_path), value_or_data=0)
    dp.fill_carrier_pressure_data(str(input_path), pressure_value_bar=0)

    # Impose carriers data (comment these lines if already defined)
    model.carrier_data_definition(f"{pathway}/{year}", str(input_path))
    model.carbon_costs_definition(f"{pathway}/{year}", str(input_path))

    # Solver options definition
    # model.solver_options_definition(input_path)
    # Optimization options definition
    model.optimization_options_definition(f"{pathway}/{year}", str(input_path))

    # Construct and solve the model
    pyhub = ModelHub()
    pyhub.read_data(str(input_path))

    # Check time to solve

    start_time = time.time()

    pyhub.quick_solve(case_study=year)

    _copy_results_to_canonical_path(
        Path(pyhub.last_solve_info["result_folder_path"]), pathway, year
    )

    end_time = time.time()
    print(f"\n\nTime to solve: {end_time - start_time} seconds")

    # # Add values of (part of) the parameters and variables to the summary file
    # add_values_to_summary(Path("output/Summary.xlsx"))

pathway = "base_case_no_ntw_5_dd"
years = ["2020", "2025", "2030", "2040", "2050"]

for index, year in enumerate(years):
    case_study_dir = Path("case_studies") / pathway / year
    if not case_study_dir.exists():
        raise ValueError(f"Year {year} does not exist in the pathway folder: {case_study_dir}")

    if index > 0:
        print(f"Setting up case study for {year}...")
        setup_brownfield(pathway, year)
        setup_emissions_limits(pathway, year)
    else:
        # on first year, check if output path already exists and if it does, raise an error to avoid overwriting results if it is not empty
        output_dir = Path("output") / pathway
        if output_dir.exists() and any(output_dir.iterdir()):
            raise FileExistsError(f"Output directory already exists for the pathway: {output_dir}. Please remove or rename it before running the first year.")

    print(f"Running case study for {year}...")
    run_path(pathway, year)
