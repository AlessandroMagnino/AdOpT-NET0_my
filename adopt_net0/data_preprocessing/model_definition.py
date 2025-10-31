import pandas as pd
import json
from pathlib import Path


def input_parameters():
    # Define input parameters here
    
    nodes_df = pd.read_csv(f"plants_data/europe_filtered_plants.csv")
    nodes_df = nodes_df.sample(n=3, random_state=42)
    nodes = nodes_df['uid'].tolist()

    periods = ['2022']

    carriers = ['electricity']

    existing_networks = ['electricityOnshore']
    new_networks = []

    parameters = {
        'nodes': nodes,
        'periods': periods,
        'carriers': carriers,
        'existing_networks': existing_networks,
        'new_networks': new_networks
    }

    return parameters


def topology_definition(input_path: Path | str):
    # Define the network topology here

    topology_path = Path(f"{input_path}/Topology.json")
    topology = json.loads((topology_path).read_text())
    
    # plants nodes
    nodes = input_parameters()['nodes']

    topology['nodes'] = nodes

    # define carriers
    carriers = input_parameters()['carriers']
    topology['carriers'] = carriers

    # define periods
    periods = input_parameters()['periods']
    topology['investment_periods'] = periods

    # simulation dates
    start_date = f"{periods[0]}-01-01 00:00"
    end_date = f"{periods[0]}-12-31 23:00"
    topology['start_date'] = start_date
    topology['end_date'] = end_date

    # Save the updated topology back to the file
    topology_path.write_text(json.dumps(topology, indent=2))

    return


def node_locations_definition(input_path: Path | str):
    # Define the node locations here

    node_locations_path = Path(f"{input_path}/NodeLocations.csv")
    node_locations_df = pd.read_csv(node_locations_path, sep=';', index_col=0)

    # plants nodes
    nodes_df = pd.read_csv(f"plants_data/europe_filtered_plants.csv")

    # Topology nodes
    topology_path = Path(f"{input_path}/Topology.json")
    topology = json.loads((topology_path).read_text())
    topology_nodes = topology['nodes']

    for node in topology_nodes:
        if node not in nodes_df['uid'].values:
            raise ValueError(f"Node {node} not found in NodeLocations.csv")
        else:
            node_locations_df.loc[node, 'lat'] = nodes_df.loc[nodes_df['uid'] == node, 'latitude'].values[0]
            node_locations_df.loc[node, 'lon'] = nodes_df.loc[nodes_df['uid'] == node, 'longitude'].values[0]
            node_locations_df.loc[node, 'alt'] = nodes_df.loc[nodes_df['uid'] == node, 'altitude'].values[0]

    node_locations_df.to_csv(node_locations_path, sep=';')

    return


def networks_definition(input_path: Path | str):
    # Define the networks here

    period = input_parameters()['periods'][0]
    networks_path = Path(f"{input_path}/{period}/Networks.json")

    networks = json.loads((networks_path).read_text())
    networks['existing'] = input_parameters()['existing_networks']
    networks['new'] = input_parameters()['new_networks']

    networks_path.write_text(json.dumps(networks, indent=2))

    # Creating needed folders for network topology
    ntw_top_path = Path(f"{input_path}/{period}/network_topology")
    for nwt in input_parameters()['existing_networks']:
        (ntw_top_path / 'existing' / nwt).mkdir(parents=True, exist_ok=True)
    for nwt in input_parameters()['new_networks']:
        (ntw_top_path / 'new' / nwt).mkdir(parents=True, exist_ok=True)

    return