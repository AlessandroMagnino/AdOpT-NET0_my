from pathlib import Path
import pandas as pd
import json

def topology_definition(input_path: Path |str):
    '''
    Fill Topology.json with nodes, carriers, and periods'''

    # Topology file path
    topology_path = Path(input_path) / "Topology.json"
    topology = json.loads(topology_path.read_text())

    # Get nodes list
    nodes = nodes_list()
    # Write nodes to topology
    topology['nodes'] = nodes

    # Get carriers list
    carriers = carriers_list()
    # Write carriers to topology
    topology['carriers'] = carriers

    # Get periods list
    periods = periods_list()
    # Write periods to topology
    topology['investment_periods'] = periods
    topology['start_date'] = f'{periods[0]}-01-01 00:00'
    topology['end_date'] = f'{periods[0]}-12-31 23:00'

    # Save topology file
    topology_path.write_text(json.dumps(topology, indent=2))

    return



def nodes_list():
    '''
    Take nodes list from plants_clusters_summary.csv
    In case, select a subset of nodes for the example
    '''
    
    # all nodes df upload
    nodes_df = pd.read_csv(f"plants_data/plants_clusters_summary.csv")

    # # ------- Remove these lines to use all nodes -------
    # # Select a subset of nodes for the example
    # uids = ['GAPTBEL0007', 'GAPTNLD0015', 'GAPTDEU0015']
    # nodes_df = nodes_df[nodes_df['uid'].isin(uids)]

    # Create nodes list from dataframe
    nodes = nodes_df['cluster'].tolist()

    return nodes


def carriers_list():
    '''
    Define carriers list
    '''
    carriers = [
        'electricity',
        'hydrogen',
        'methane',
        'heat',
        'CO2',
        'nitrogen',
        'HBfeed',
        'steam',
        'ammonia',
        'naphtha',
        'olefins',
        'ethylene',
        'propylene',
        'crackergas',
        'syngas',
        'methanol',
        'MPW'
        ]
    
    return carriers


def periods_list():
    '''
    Define periods list
    '''
    periods = ['2022']
    
    return periods