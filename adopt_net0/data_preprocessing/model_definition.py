import pandas as pd
import json
from pathlib import Path

def topology_definition(input_path: Path | str):
    # Define the network topology here

    topology_path = Path(f"{input_path}/Topology.json")
    topology = json.loads((topology_path).read_text())
    
    # plants nodes
    nodes_df = pd.read_csv(f"plants_data/europe_filtered_plants.csv")
    # filter on 3 random plants for testing
    nodes_df = nodes_df.sample(n=3, random_state=42)

    topology['nodes'] = nodes_df['uid'].tolist()

    # define carriers
    carriers = ['electricity']
    topology['carriers'] = carriers

    # define periods
    periods = ['2022']
    topology['investment_periods'] = periods

    # simulation dates
    start_date = "2022-01-01 00:00"
    end_date = "2022-12-31 23:00"
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