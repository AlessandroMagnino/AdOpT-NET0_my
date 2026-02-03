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

    # # ASU
    # additional_tech_spec['ASU'] = {
    #     'Economics': {
    #         'capex_model': 1,
    #         'unit_capex': 1300000,
    #         'fix_capex': 0,
    #         'opex_fixed': 0.02
    #     },
    #     'Performance': {
    #         'performance_function_type': 1,
    #         'min_part_load': 0 # ASU can operate from 0% to 100% of its capacity if 0
    #     }
    # }

    # HBfeed_mixer
    additional_tech_spec['HBfeed_mixer'] = {
        "Units": {
            "size": "MW",
            "input_carrier": {
                "hydrogen": "MW",
                "nitrogen": "tonne/hr"
                },
                "output_carrier": {
                    "HBfeed": "MW"
                }
        }
    }


    # HB
    additional_tech_spec['HaberBosch'] = {
        'Economics': {
            'capex_model': 1,
            'unit_capex': 3400000,
            'fix_capex': 0,
            'opex_fixed': 0.02
        },
        'Performance': {
            'performance_function_type': 1,
            'min_part_load': 0.8 # HB can operate from 0% to 100% of its capacity if 0
        },
        'Units': {
            'size': 'tonne/hr'
        }
    }

    # SteamReformer
    additional_tech_spec['SteamReformer'] = {
        'Economics': {
            'capex_model': 1,
            'unit_capex': 800000,
            'fix_capex': 0
        },
        'Performance': {
            # 'min_part_load': 0, # SteamReformer can operate from 0% to 100% of its capacity if 0
            'input_carrier': ['methane', 'steam'], # not feedgas+steam as default
            'main_input_carrier': 'methane',
            'input_ratios': {
                'methane': 1.0,
                'steam': 0.087
            }  # methane:steam ratio
        },
        'Units': {
            'input_carrier': {
                'methane': 'tonne/hr',
                'steam': 'MW'
            }  # specify that input_ratios are in fraction
        }
    }

    # # Boiler_El
    # additional_tech_spec['Boiler_El'] = {
    #     'Economics': {
    #         'fix_capex': 0,
    #         'unit_capex': 153704
    #     },
    #     'Performance': {
    #         'performance_function_type': 1,
    #         'output_carrier': ['steam'],
    #         'min_part_load': 0,
    #         'performance': {
    #             'in': [
    #                 0,
    #                 1
    #             ],
    #             'out': {
    #                 'steam': [
    #                 0,
    #                 0.99
    #             ]}
    #         }
    #     },
    #     'Units': {
    #         'output_carrier': {
    #             'steam': 'MW'
    #         }
    #     }
    # }

    # eSMR_H2
    additional_tech_spec['eSMR_H2'] = {
        'Performance': {
            'input_carrier': ['methane', 'electricity'], # not feedgas+electricity as default
            'main_input_carrier': 'methane',
            'input_ratios': {
                'methane': 1.0,
                'electricity': 0.272
            }  # methane:electricity ratio
        },
        'Units': {
            'input_carrier': {
                'methane': 'tonne/hr',
                'electricity': 'MW'
            }  # specify that input_ratios are in fraction
        }
    }

    # eSMR_syngas
    additional_tech_spec['eSMR_syngas'] = {
        # 'Economics': {
        #     'capex_model': 3,
        #     'unit_capex': 524673,
        #     'fix_capex': 126718694
        # },
        'Economics': {
            'capex_model': 1,
            'unit_capex': 800000,
            'fix_capex': 0
        },
        'Performance': {
            'performance_function_type': 1,
            'min_part_load': 0.4,
            'input_carrier': ['methane', 'electricity'], # not feedgas+electricity as default
            'main_input_carrier': 'methane',
            'input_ratios': {
                'methane': 1.0,
                'electricity': 0.272
            }  # methane:electricity ratio
        },
        'Units': {
            'input_carrier': {
                'methane': 'tonne/hr',
                'electricity': 'MW'
            }  # specify that input_ratios are in fraction
        }
    }

    # Electrolyzer
    additional_tech_spec['Electrolyzer'] = {
        'Economics': {
            'capex_model': 1,
            'unit_capex': 1200000,
            'fix_capex': 0
        },
        'Performance': {
            'performance_function_type': 1,
            'min_part_load': 0, # Electrolyzer can operate from 0% to 100% of its capacity if 0
            'performance': {
                        'in': [
                            0,
                            1
                        ],
                        'out':
                            [0, 
                            0.6]
                    }
        }
    }

    # CrackerFurnace
    additional_tech_spec['CrackerFurnace'] = {
        'Economics': {
            'capex_model': 1,
            'unit_capex': 458000,
            'fix_capex': 0
        },
        'Performance': {
            'min_part_load': 0.4
        },
        'Units': {
            'size': 'tonne/hr',
            'input_carrier': {
                'naphtha': 'tonne/hr',
                'steam': 'MW',
                'electricity': 'MW'
            }
        }
    }

    # # eCrackerFurnace
    # additional_tech_spec['eCrackerFurnace'] = {
    #     'Economics': {
    #         'capex_model': 1,
    #         'unit_capex': 458000,
    #         'fix_capex': 0
    #     },
    #     'Performance': {
    #         'performance_function_type': 1,
    #         'min_part_load': 0.4 # eCrackerFurnace can operate from 0% to 100% of its capacity if 0
    #     },
    #     'Units': {
    #         'size': 'tonne/hr',
    #         'input_carrier': {
    #             'naphtha': 'tonne/hr',
    #             'electricity': 'MW'
    #         }
    #     }
    # }

    # # MeOHsynthesis
    # additional_tech_spec['MeOHsynthesis'] = {
    #     'Economics': {
    #         'capex_model': 1,
    #         'unit_capex': 1000000,
    #         'fix_capex': 0
    #     },
    #     'Performance': {
    #         'performance_function_type': 1,
    #         'min_part_load': 0.4
    #     }
    # }

    # # MethanolToOlefins
    # additional_tech_spec['MethanolToOlefins'] = {
    #     'Economics': {
    #         'capex_model': 1,
    #         'unit_capex': 1200000,
    #         'fix_capex': 0
    #     },
    #     'Performance': {
    #         'performance_function_type': 1,
    #         'min_part_load': 0.4
    #     }
    # }

    # OlefinSeparation
    additional_tech_spec['OlefinSeparation'] = {
        'Economics': {
            'capex_model': 1,
            'unit_capex': 1200000,
            'fix_capex': 0
        }
    }

    # Plastic2methanol
    additional_tech_spec['Plastic2methanol'] = {
        'Economics': {
            'capex_model': 1,
            'unit_capex': 1500000,
            'fix_capex': 0
        }
    }

    # rWGS
    additional_tech_spec['rWGS'] = {
        'Performance': {
            'performance_function_type': 1,
            'min_part_load': 0
        },
        'Economics': {
            'capex_model': 1,
            'unit_capex': 500000,
            'fix_capex': 0
        }
    }

    return additional_tech_spec