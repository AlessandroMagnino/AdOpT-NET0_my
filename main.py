# from adopt_net0.model_configuration import ModelConfiguration
from pathlib import Path
import adopt_net0.data_preprocessing as dp
import adopt_net0.database as db
import adopt_net0.data_preprocessing.model_definition as model
from adopt_net0.modelhub import ModelHub
from adopt_net0.result_management.read_results import add_values_to_summary

# Specify the path to your input data
input_path = "input"
output_path = "output"

# Create template files (comment these lines if already defined)
dp.create_optimization_templates(input_path, output_path)

# Topology definition
model.topology_definition(input_path)

# Create folder structure (comment these lines if already defined)
dp.create_input_data_folder_template(input_path)

# Define nodes locations (comment these lines if already defined)
model.nodes_location_definition(input_path)

# Define networks (comment these lines if already defined)
model.networks_definition(input_path)

# Define technologies on each node (comment these lines if already defined)
model.technologies_definition(input_path)

# Copy technology and network data into folder (comment these lines if already defined)
dp.copy_technology_data(input_path)
dp.copy_network_data(input_path)
dp.copy_compressor_data(input_path)

# Read climate data and fill carried data (comment these lines if already defined)
dp.load_climate_data_from_api(input_path)
dp.fill_carrier_data(input_path, value_or_data=0)
dp.fill_carrier_pressure_data(input_path, pressure_value_bar=0)

# Impose carriers data (comment these lines if already defined)
model.carrier_data_definition(input_path)

# Output path definition
dp.config_model_correction(input_path, output_path)

# Construct and solve the model
pyhub = ModelHub()
pyhub.read_data(input_path)
pyhub.quick_solve()

# Add values of (part of) the parameters and variables to the summary file
add_values_to_summary(Path("output/Summary.xlsx"))
