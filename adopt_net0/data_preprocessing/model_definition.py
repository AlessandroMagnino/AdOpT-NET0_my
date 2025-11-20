from pathlib import Path
import pandas as pd
import numpy as np
import json
import random


def input_parameters():
    # Define input parameters here
    
    nodes_df = pd.read_csv(f"plants_data/europe_filtered_plants.csv")
    # Select a subset of nodes for the example
    uids = ['GAPTBEL0007', 'GAPTNLD0015', 'GAPTDEU0015']
    nodes_df = nodes_df[nodes_df['uid'].isin(uids)]
    nodes = nodes_df['uid'].tolist()

    periods = ['2022']

    carriers = ['electricity', 'hydrogen']

    existing_networks = ['electricitySimple', 'hydrogenSimple']
    new_networks = []

    connections_possible = {}
    connections_possible['electricitySimple'] = 1
    connections_possible['hydrogenSimple'] = 1

    existing_technologies = ['Photovoltaic', 'WindTurbine_Onshore_1500']
    new_technologies = ['Photovoltaic', 'WindTurbine_Onshore_1500', 'Storage_Battery', 'Electrolyzer']

    carriers_data = {}
    carriers_data = {
        'electricity': {
            'Demand': 1, # MW
            'Import limit': 1000,
            'Export limit': [pd.NA],
            'Import price': 'plants_data/electricity_prices_2024.csv',
            'Export price': [pd.NA],
            'Import emission factor': [pd.NA],
            'Export emission factor': [pd.NA],
            'Generic production': [pd.NA]
        },
        'hydrogen': {
            'Demand': 1, # MW
            'Import limit': 0,
            'Export limit': [pd.NA],
            'Import price': [pd.NA],
            'Export price': [pd.NA],
            'Import emission factor': [pd.NA],
            'Export emission factor': [pd.NA],
            'Generic production': [pd.NA]
        }
    }

    parameters = {
        'nodes': nodes,
        'periods': periods,
        'carriers': carriers,
        'existing_networks': existing_networks,
        'new_networks': new_networks,
        'connections_possible': connections_possible,
        'existing_technologies': existing_technologies,
        'new_technologies': new_technologies,
        'carriers_data': carriers_data
    }

    return parameters


# def topology_definition(input_path: Path | str):
#     # Define the network topology here

#     topology_path = Path(f"{input_path}/Topology.json")
#     topology = json.loads((topology_path).read_text())
    
#     # plants nodes
#     nodes = input_parameters()['nodes']

#     topology['nodes'] = nodes

#     # define carriers
#     carriers = input_parameters()['carriers']
#     topology['carriers'] = carriers

#     # define periods
#     periods = input_parameters()['periods']
#     topology['investment_periods'] = periods

#     # simulation dates
#     start_date = f"{periods[0]}-01-01 00:00"
#     end_date = f"{periods[0]}-12-31 23:00"
#     topology['start_date'] = start_date
#     topology['end_date'] = end_date

#     # Save the updated topology back to the file
#     topology_path.write_text(json.dumps(topology, indent=8))

#     return


# def node_locations_definition(input_path: Path | str):
#     # Define the node locations here

#     node_locations_path = Path(f"{input_path}/NodeLocations.csv")
#     node_locations_df = pd.read_csv(node_locations_path, sep=';', index_col=0)

#     # plants nodes
#     nodes_df = pd.read_csv(f"plants_data/europe_filtered_plants.csv")

#     # Topology nodes
#     topology_path = Path(f"{input_path}/Topology.json")
#     topology = json.loads((topology_path).read_text())
#     topology_nodes = topology['nodes']

#     for node in topology_nodes:
#         if node not in nodes_df['uid'].values:
#             raise ValueError(f"Node {node} not found in NodeLocations.csv")
#         else:
#             node_locations_df.loc[node, 'lat'] = nodes_df.loc[nodes_df['uid'] == node, 'latitude'].values[0]
#             node_locations_df.loc[node, 'lon'] = nodes_df.loc[nodes_df['uid'] == node, 'longitude'].values[0]
#             node_locations_df.loc[node, 'alt'] = nodes_df.loc[nodes_df['uid'] == node, 'altitude'].values[0]

#     node_locations_df.to_csv(node_locations_path, sep=';')

#     return


# def networks_definition(input_path: Path | str):
#     # Define the networks here

#     period = input_parameters()['periods'][0]
#     networks_path = Path(f"{input_path}/{period}/Networks.json")

#     networks = json.loads((networks_path).read_text())
#     networks['existing'] = input_parameters()['existing_networks']
#     networks['new'] = input_parameters()['new_networks']

#     networks_path.write_text(json.dumps(networks, indent=2))

#     # Creating needed folders for network topology
#     ntw_top_path = Path(f"{input_path}/{period}/network_topology")
#     for nwt in input_parameters()['existing_networks']:
#         (ntw_top_path / 'existing' / nwt).mkdir(parents=True, exist_ok=True)
#     for nwt in input_parameters()['new_networks']:
#         (ntw_top_path / 'new' / nwt).mkdir(parents=True, exist_ok=True)

#     return


# def networks_topology_definition(input_path: Path | str):
#     # Define the network topology here

#     nodes = input_parameters()['nodes']
#     existing_networks = input_parameters()['existing_networks']
#     new_networks = input_parameters()['new_networks']
#     dist_data_df = pd.read_csv(f"plants_data/plants_distance_matrix.csv", sep=';', index_col=0)

#     for nwt in existing_networks:
#         conn_path = Path(f"{input_path}/{input_parameters()['periods'][0]}/network_topology/existing/{nwt}/connection.csv")
#         dist_path = Path(f"{input_path}/{input_parameters()['periods'][0]}/network_topology/existing/{nwt}/distance.csv")
#         size_path = Path(f"{input_path}/{input_parameters()['periods'][0]}/network_topology/existing/{nwt}/size.csv")
#         connection = input_parameters()['connections_possible'][nwt]
#         conn_df = pd.DataFrame(index=nodes, columns=nodes)
#         dist_df = pd.DataFrame(index=nodes, columns=nodes)
#         size_df = pd.DataFrame(index=nodes, columns=nodes)
#         for i in nodes:
#             for j in nodes:
#                 if i != j:
#                     conn_df.loc[i, j] = connection
#                     dist_df.loc[i, j] = dist_data_df.loc[i, j] * connection
#                     size_df.loc[i, j] = 1000  # [MW] Example fixed size, modify as needed
#                 else:
#                     conn_df.loc[i, j] = 0
#                     dist_df.loc[i, j] = 0
#                     size_df.loc[i, j] = 0
#         conn_df.to_csv(conn_path, sep=';')
#         dist_df.to_csv(dist_path, sep=';')
#         size_df.to_csv(size_path, sep=';')

#     for nwt in new_networks:
#         conn_path = Path(f"{input_path}/{input_parameters()['periods'][0]}/network_topology/new/{nwt}/connection.csv")
#         dist_path = Path(f"{input_path}/{input_parameters()['periods'][0]}/network_topology/new/{nwt}/distance.csv")
#         size_path = Path(f"{input_path}/{input_parameters()['periods'][0]}/network_topology/new/{nwt}/size_max_arcs.csv")
#         connection = input_parameters()['connections_possible'][nwt]
#         conn_df = pd.DataFrame(index=nodes, columns=nodes)
#         dist_df = pd.DataFrame(index=nodes, columns=nodes)
#         size_df = pd.DataFrame(index=nodes, columns=nodes)
#         for i in nodes:
#             for j in nodes:
#                 if i != j:
#                     conn_df.loc[i, j] = connection
#                     dist_df.loc[i, j] = dist_data_df.loc[i, j] * connection
#                     size_df.loc[i, j] = 10000  # [MW] Example fixed size, modify as needed
#                 else:
#                     conn_df.loc[i, j] = 0
#                     dist_df.loc[i, j] = 0
#                     size_df.loc[i, j] = 0
#         conn_df.to_csv(conn_path, sep=';')
#         dist_df.to_csv(dist_path, sep=';')
#         size_df.to_csv(size_path, sep=';')

#     return


# def technologies_definition(input_path: Path | str):

#     period = input_parameters()['periods'][0]
#     nodes = input_parameters()['nodes']
#     existing_technologies = input_parameters()['existing_technologies']
#     new_technologies = input_parameters()['new_technologies']

#     for node in nodes[:-1]:
#         tech_path = Path(f"{input_path}/{period}/node_data/{node}/Technologies.json")
#         technologies = json.loads((tech_path).read_text())
#         technologies['existing'] = {tec: random.randint(0, 2) for tec in existing_technologies}
#         technologies['new'] = list(new_technologies)
#         tech_path.write_text(json.dumps(technologies, indent=2))

#     # Last node with only new technologies
#     node = nodes[-1]
#     tech_path = Path(f"{input_path}/{period}/node_data/{node}/Technologies.json")
#     technologies = json.loads((tech_path).read_text())
#     technologies['existing'] = {}
#     technologies['new'] = new_technologies
#     tech_path.write_text(json.dumps(technologies, indent=2))

#     return


def carrier_data_definition(input_path: Path | str):
    # Define carrier data here

    nodes = input_parameters()['nodes']
    period = input_parameters()['periods'][0]
    carrier_params = input_parameters()['carriers_data']['electricity']

    for node in nodes:
        carrier_data_path = Path(f"{input_path}/{period}/node_data/{node}/carrier_data")
        carrier_data_df = pd.read_csv(carrier_data_path / "electricity.csv", sep=';', index_col=0)

        for param, value in carrier_params.items():
            if param == 'Import price' and value is str:
                price_df = pd.read_csv(value, sep=';', index_col=0)
                carrier_data_df[param] = price_df['Netherlands (EUR/MWh)'].values
            elif param != 'Import price' and value:
                carrier_data_df[param] = np.full(len(carrier_data_df), value)
            else:
                # leave column empty if None
                carrier_data_df[param] = pd.NA

        carrier_data_df.to_csv(carrier_data_path / "electricity.csv", sep=';')

    carrier_params = input_parameters()['carriers_data']['hydrogen']

    for node in nodes:
        carrier_data_path = Path(f"{input_path}/{period}/node_data/{node}/carrier_data")
        carrier_data_df = pd.read_csv(carrier_data_path / "hydrogen.csv", sep=';', index_col=0)

        for param, value in carrier_params.items():
            if value:
                carrier_data_df[param] = np.full(len(carrier_data_df), value)
            else:
                # leave column empty if None
                carrier_data_df[param] = pd.NA

        carrier_data_df.to_csv(carrier_data_path / "hydrogen.csv", sep=';')

    return


# def config_model_correction(input_path: Path | str, output_path: Path | str):
#     """
#     Correct the output path in ConfigModel.json file.
#     :param folder_path: Path to the folder where ConfigModel.json is located (if not provided, an
#     :return: None
#     """

#     config_file_path = Path(f"{input_path}/ConfigModel.json")
#     config = json.loads((config_file_path).read_text())
#     config['reporting']['save_summary_path']['value'] = './' + str(output_path) + '/'
#     config['reporting']['save_path']['value'] = './' + str(output_path) + '/'

#     config['optimization']['typicaldays']['N']['value'] = 30
#     config['optimization']['typicaldays']['method']['value'] = 1
#     config['solveroptions']['mipgap']['value'] = 0.01

#     config_file_path.write_text(json.dumps(config, indent=4))

#     return
