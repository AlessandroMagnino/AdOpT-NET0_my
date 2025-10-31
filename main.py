# from adopt_net0.model_configuration import ModelConfiguration
from pathlib import Path
import adopt_net0.data_preprocessing as dp
from adopt_net0.modelhub import ModelHub
from adopt_net0.result_management.read_results import add_values_to_summary

# Specify the path to your input data
input_path = "input"

# Create template files (comment these lines if already defined)
dp.create_optimization_templates(input_path)

# Topology definition
dp.topology_definition(input_path)

# Create folder structure (comment these lines if already defined)
dp.create_input_data_folder_template(input_path)

# Define nodes locations (comment these lines if already defined)
dp.node_locations_definition(input_path)

# Define networks (comment these lines if already defined)
dp.networks_definition(input_path)

# # Copy technology and network data into folder (comment these lines if already defined)
# dp.copy_technology_data(input_path, "path to tec data")
# dp.copy_network_data(input_path, "path to network data")
# dp.copy_compressor_data(input_path, "path to compressor data")

# # Read climate data and fill carried data (comment these lines if already defined)
# dp.load_climate_data_from_api(input_path)
# dp.fill_carrier_data(input_path, value=0)
# # dp.fill_carrier_pressure_data(input_path, value=0)

# # Construct and solve the model
# pyhub = ModelHub()
# pyhub.read_data(input_path)
# pyhub.quick_solve()

# # Add values of (part of) the parameters and variables to the summary file
# add_values_to_summary(Path("path to summary file"))
