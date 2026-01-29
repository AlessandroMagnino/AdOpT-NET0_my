from pathlib import Path
import json

def networks_data_correction(input_path):
    '''
    Correct some networks data if needed
    '''

    # Topology, nodes and periods
    topology_path = Path(input_path) / "Topology.json"
    topology = json.loads(topology_path.read_text())
    periods = topology['investment_periods']

    additional_ntws_spec = additional_networks_spec()

    for period in periods:
        network_data_path = Path(input_path) / f"{period}" / "network_data"

        # List of all the .json files in network_data folder, creating list removing .json from filename
        network_files = [f.stem for f in network_data_path.glob("*.json")]

        # Example correction: ensure all lines have a 'max_capacity' field
        for line in network_files:
            network_file_path = network_data_path / f"{line}.json"
            network_data = json.loads(network_file_path.read_text())

            # If the network is in additional_networks_spec, update its data
            if line in additional_ntws_spec:
                for section, specs in additional_ntws_spec[line].items():
                    if section not in network_data:
                        network_data[section] = {}
                    network_data[section].update(specs)
                
                # Save the updated network data
                network_file_path.write_text(json.dumps(network_data, indent=4))

    return


def additional_networks_spec():
    '''
    Define additional networks specifications if needed
    '''

    additional_networks_spec = {}

    # # electricitySimple
    # additional_networks_spec['electricitySimple'] = {
    #     'Performance': {
    #         'bidirectional_network': 1, #https://adopt-net0.readthedocs.io/en/latest/src_code/model_components/networks.html
    #         'bidirectional_network_precise': 0
    #     }
    # }

    # # electricityOnshore
    # additional_networks_spec['electricityOnshore'] = {
    #     'Performance': {
    #         'bidirectional_network': 1, #https://adopt-net0.readthedocs.io/en/latest/src_code/model_components/networks.html
    #         'bidirectional_network_precise': 0 # Allow flow reversal if 1
    #     }
    # }

    # # hydrogenSimple
    # additional_networks_spec['hydrogenSimple'] = {
    #     'Performance': {
    #         'bidirectional_network': 0, #https://adopt-net0.readthedocs.io/en/latest/src_code/model_components/networks.html
    #         'bidirectional_network_precise': 0 # Allow flow reversal if 1
    #     }
    # }

    # hydrogenPipelineOnshore
    additional_networks_spec['hydrogenPipelineOnshore'] = {
        'Performance': {
            'bidirectional_network': 0, #https://adopt-net0.readthedocs.io/en/latest/src_code/model_components/networks.html
            'bidirectional_network_precise': 0, # Allow flow reversal if 1
            'min_transport': 0 # Minimum transport activity of the network
        },
        'Economics': {
            'gamma1': 0,  # no CAPEX constant term
            'gamma2': 0,   # no size dependency
            'gamma3': 1000, # EUR/km
            'gamma4': 0    # no size*distance dependency
        }
    }

    return additional_networks_spec