from pathlib import Path
import pandas as pd
import json

def technologies_data_correction(input_path):
    '''
    Correct some technologies data if needed
    '''

    # Topology, nodes and periods
    topology_path = Path(input_path) / "Topology.json"
    topology = json.loads(topology_path.read_text())
    nodes = topology['nodes']
    periods = topology['investment_periods']

    additional_tech_spec = additional_technologies_spec()

    for period in periods:
        for node in nodes:
            tech_data_path = Path(input_path) / f"{period}" / "node_data" / node / 'technology_data'

            # List of all the .json files in technology_data folder, creating list removing .json from filename
            tech_files = [f.stem for f in tech_data_path.glob("*.json")]

            for tech in tech_files:
                tech_file_path = tech_data_path / f"{tech}.json"
                tech_data = json.loads(tech_file_path.read_text())

                # If the technology is in additional_tech_spec, update its data
                if tech in additional_tech_spec:
                    for section, specs in additional_tech_spec[tech].items():
                        if section not in tech_data:
                            tech_data[section] = {}
                        tech_data[section].update(specs)
                    
                    # Save the updated technology data
                    tech_file_path.write_text(json.dumps(tech_data, indent=4))

    return



def additional_technologies_spec():
    '''
    Define additional technologies specifications if needed
    '''

    additional_tech_spec = {}

    # Battery
    additional_tech_spec['Storage_Battery'] = {
        'Performance': {
            'allow_only_one_direction': 0 # Battery can charge and discharge in the same time if 0
        }
    }

    # H2 storage
    additional_tech_spec['Storage_H2'] = {
        'Performance': {
            'allow_only_one_direction': 0 # H2 storage cannot charge and discharge in the same time if 1
        }
    }

    # ASU
    additional_tech_spec['ASU'] = {
        'Performance': {
            'min_part_load': 0 # ASU can operate from 0% to 100% of its capacity if 0
        }
    }

    # # HB
    # additional_tech_spec['HaberBosch'] = {
    #     'Performance': {
    #         'min_part_load': 0 # HB can operate from 0% to 100% of its capacity if 0
    #     }
    # }

    # SteamReformer
    additional_tech_spec['SteamReformer'] = {
        'Performance': {
            # 'min_part_load': 0, # SteamReformer can operate from 0% to 100% of its capacity if 0
            'input_carrier': ['methane', 'steam'], # not feedgas+steam as default
            'main_input_carrier': 'methane'
        }
    }


    return additional_tech_spec