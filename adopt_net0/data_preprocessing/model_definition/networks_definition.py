from pathlib import Path
import pandas as pd
import json

def networks_definition(input_path: Path | str):
    '''
    Fill Networks.json for each investment period
    '''

    # Topology
    topology_path = Path(input_path) / "Topology.json"
    topology = json.loads(topology_path.read_text())
    periods = topology['investment_periods']

    # Networks
    existing_networks, new_networks = networks_list()

    # Fill Networks.json for each period
    networks_file_definition(input_path, periods, existing_networks, new_networks)

    # Network topology definition
    network_topology_definition(input_path, periods, existing_networks, new_networks)

    return


def networks_file_definition(input_path: Path | str, periods: list, existing_networks: list, new_networks: list):
    '''
    Fill Networks.json for a specific investment period
    '''

    # At the moment, we cannot define different networks for different periods
    for period in periods:
        # Networks file path
        networks_path = Path(input_path) / f"{period}" / "Networks.json"
        networks = json.loads(networks_path.read_text())

        # Write existing networks
        networks['existing'] = existing_networks
        # Write new networks
        networks['new'] = new_networks

        # Save Networks file
        networks_path.write_text(json.dumps(networks, indent=2))
    
        # Creating needed folders for network topology
        network_topology_path = Path(input_path) / f"{period}" / 'network_topology'
        for ntw in existing_networks:
            (network_topology_path / 'existing' / ntw).mkdir(parents=True, exist_ok=True)
        for ntw in new_networks:
            (network_topology_path / 'new' / ntw).mkdir(parents=True, exist_ok=True)

    return


def network_topology_definition(input_path: Path | str, periods: list, existing_networks: list, new_networks: list):
    '''
    Fill network topology for each network in each investment period, creating needed matrix files
    '''

    topology = json.loads((Path(input_path) / "Topology.json").read_text())
    nodes = topology['nodes']

    for period in periods:
        for ntw in existing_networks:
            conn_file_path = Path(input_path) / f"{period}" / 'network_topology' / 'existing' / ntw / 'connection.csv'
            dist_file_path = Path(input_path) / f"{period}" / 'network_topology' / 'existing' / ntw / 'distance.csv'
            exist_size_file_path = Path(input_path) / f"{period}" / 'network_topology' / 'existing' / ntw / 'size.csv'
            max_size_file_path = Path(input_path) / f"{period}" / 'network_topology' / 'existing' / ntw / 'size_max_arcs.csv'

            dfs_path = 'plants_data'
            conn_data = pd.read_excel(Path(dfs_path) / f'{ntw}.xlsx', sheet_name='connection', index_col=0)
            dist_data = pd.read_excel(Path(dfs_path) / f'{ntw}.xlsx', sheet_name='distances', index_col=0)
            exist_size_data = pd.read_excel(Path(dfs_path) / f'{ntw}.xlsx', sheet_name='existing_sizes', index_col=0)
            max_size_data = pd.read_excel(Path(dfs_path) / f'{ntw}.xlsx', sheet_name='maximum_sizes', index_col=0)

            conn_df = pd.DataFrame(0, index=nodes, columns=nodes)
            dist_df = pd.DataFrame(0, index=nodes, columns=nodes)
            exist_size_df = pd.DataFrame(0, index=nodes, columns=nodes)
            max_size_df = pd.DataFrame(0, index=nodes, columns=nodes)

            for node_i in nodes:
                for node_j in nodes:
                    if node_i not in conn_data.index or node_j not in conn_data.columns:
                        raise ValueError(f"Connection matrix for network {ntw} is missing node {node_i} or {node_j}. Please update the connection matrix.")
                    conn_df.loc[node_i, node_j] = conn_data.loc[node_i, node_j]
                    if node_i not in dist_data.index or node_j not in dist_data.columns:
                        raise ValueError(f"Distance matrix for network {ntw} is missing node {node_i} or {node_j}. Please update the distance matrix.")
                    dist_df.loc[node_i, node_j] = dist_data.loc[node_i, node_j]
                    if node_i not in exist_size_data.index or node_j not in exist_size_data.columns:
                        raise ValueError(f"Existing size matrix for network {ntw} is missing node {node_i} or {node_j}. Please update the existing size matrix.")
                    exist_size_df.loc[node_i, node_j] = exist_size_data.loc[node_i, node_j]
                    if node_i not in max_size_data.index or node_j not in max_size_data.columns:
                        raise ValueError(f"Max size matrix for network {ntw} is missing node {node_i} or {node_j}. Please update the max size matrix.")
                    max_size_df.loc[node_i, node_j] = max_size_data.loc[node_i, node_j]

            conn_df.to_csv(conn_file_path, sep=';')
            dist_df.to_csv(dist_file_path, sep=';')
            exist_size_df.to_csv(exist_size_file_path, sep=';')
            max_size_df.to_csv(max_size_file_path, sep=';')

        for ntw in new_networks:
            conn_file_path = Path(input_path) / f"{period}" / 'network_topology' / 'new' / ntw / 'connection.csv'
            dist_file_path = Path(input_path) / f"{period}" / 'network_topology' / 'new' / ntw / 'distance.csv'
            max_size_file_path = Path(input_path) / f"{period}" / 'network_topology' / 'new' / ntw / 'size_max_arcs.csv'

            dfs_path = 'plants_data'
            conn_data = pd.read_excel(Path(dfs_path) / f'{ntw}.xlsx', sheet_name='connection', index_col=0)
            dist_data = pd.read_excel(Path(dfs_path) / f'{ntw}.xlsx', sheet_name='distances', index_col=0)
            max_size_data = pd.read_excel(Path(dfs_path) / f'{ntw}.xlsx', sheet_name='maximum_sizes', index_col=0)

            conn_df = pd.DataFrame(0, index=nodes, columns=nodes)
            dist_df = pd.DataFrame(0, index=nodes, columns=nodes)
            max_size_df = pd.DataFrame(0, index=nodes, columns=nodes)

            for node_i in nodes:
                for node_j in nodes:
                    if node_i not in conn_data.index or node_j not in conn_data.columns:
                        raise ValueError(f"Connection matrix for network {ntw} is missing node {node_i} or {node_j}. Please update the connection matrix.")
                    conn_df.loc[node_i, node_j] = conn_data.loc[node_i, node_j]
                    if node_i not in dist_data.index or node_j not in dist_data.columns:
                        raise ValueError(f"Distance matrix for network {ntw} is missing node {node_i} or {node_j}. Please update the distance matrix.")
                    dist_df.loc[node_i, node_j] = dist_data.loc[node_i, node_j]
                    if node_i not in max_size_data.index or node_j not in max_size_data.columns:
                        raise ValueError(f"Max size matrix for network {ntw} is missing node {node_i} or {node_j}. Please update the max size matrix.")
                    max_size_df.loc[node_i, node_j] = max_size_data.loc[node_i, node_j]

            conn_df.to_csv(conn_file_path, sep=';')
            dist_df.to_csv(dist_file_path, sep=';')
            max_size_df.to_csv(max_size_file_path, sep=';')


def networks_list():
    '''
    Define networks list
    '''
    existing_networks = [
        'electricityOnshore'
    ]

    new_networks = [
        'hydrogenSimple'
    ]

    return existing_networks, new_networks