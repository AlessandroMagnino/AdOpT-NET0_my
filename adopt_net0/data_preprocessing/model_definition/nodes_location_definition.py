from pathlib import Path
import pandas as pd
import json

def nodes_location_definition(input_path: Path | str):
    '''
    Fill NodeLocations.csv with node locations
    '''

    # NodeLocations file path
    node_locations_path = Path(input_path) / "NodeLocations.csv"
    node_locations = pd.read_csv(node_locations_path, sep=';', index_col=0)

    # Topology file path
    topology_path = Path(input_path) / "Topology.json"
    topology = json.loads(topology_path.read_text())

    # Get nodes list from topology
    nodes = topology['nodes']

    # nodes_df
    nodes_df_path = Path("plants_data/plants_clusters_summary.csv")
    nodes_df = pd.read_csv(nodes_df_path)

    # Get lat, lon, alt for each node
    for node in nodes:
        if not node in nodes_df['cluster'].values:
            raise ValueError(f"Node {node} not found in plants data.")
        else:
            node_locations.loc[node, 'lat'] = nodes_df.loc[nodes_df['cluster'] == node, 'latitude'].values[0]
            node_locations.loc[node, 'lon'] = nodes_df.loc[nodes_df['cluster'] == node, 'longitude'].values[0]
            node_locations.loc[node, 'alt'] = nodes_df.loc[nodes_df['cluster'] == node, 'altitude'].values[0]

    # Save NodeLocations file
    node_locations.to_csv(node_locations_path, sep=';')

    return

