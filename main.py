# from adopt_net0.model_configuration import ModelConfiguration
from pathlib import Path
import adopt_net0.data_preprocessing as dp
import adopt_net0.database as db
import adopt_net0.data_preprocessing.model_definition as model
from adopt_net0.modelhub import ModelHub
from adopt_net0.result_management.read_results import add_values_to_summary
import time

# Specify the path to your input data
case_study = "CO2_transport_no_fossil_limited_MPW"  # "CO2_transport_no_fossil"  # "CO2_transport"
input_path = 'input'
output_path = "output"

# Create template files (comment these lines if already defined)
dp.create_optimization_templates(input_path, output_path)

# Topology definition
model.topology_definition(case_study, input_path)

# Create folder structure (comment these lines if already defined)
dp.create_input_data_folder_template(input_path)

# Define nodes locations (comment these lines if already defined)
model.nodes_location_definition(case_study, input_path)

# Define networks (comment these lines if already defined)
model.networks_definition(case_study, input_path)

# Define technologies on each node (comment these lines if already defined)
model.technologies_definition(case_study, input_path)

# Copy technology and network data into folder (comment these lines if already defined)
dp.copy_technology_data(input_path)
dp.copy_network_data(input_path)
dp.copy_compressor_data(input_path)

# Correct data on technologies and networks if needed (comment these lines if already defined)
# model.technologies_data_correction(input_path)

# Correct data on networks if needed (comment these lines if already defined)
# model.networks_data_correction(input_path)

# Read climate data and fill carried data (comment these lines if already defined)
dp.load_climate_data_from_api(input_path)
dp.fill_carrier_data(input_path, value_or_data=0)
dp.fill_carrier_pressure_data(input_path, pressure_value_bar=0)

# Impose carriers data (comment these lines if already defined)
model.carrier_data_definition(case_study, input_path)

# Solver options definition
model.solver_options_definition(input_path)
# Optimization options definition
model.optimization_options_definition(input_path)

# Construct and solve the model
pyhub = ModelHub()
pyhub.read_data(input_path)

# Check time to solve

start_time = time.time()

pyhub.quick_solve(case_study=case_study)

end_time = time.time()
print(f"\n\nTime to solve: {end_time - start_time} seconds")

# # Add values of (part of) the parameters and variables to the summary file
# add_values_to_summary(Path("output/Summary.xlsx"))


