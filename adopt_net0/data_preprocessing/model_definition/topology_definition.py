from pathlib import Path
import re
import pandas as pd
import json

def topology_definition(case_study: Path |str,
                        input_path: Path | str):
    '''
    Fill Topology.json with nodes, carriers, and periods'''

    # Topology file path
    topology_path = Path(input_path) / "Topology.json"
    topology = json.loads(topology_path.read_text())

    # Get nodes list
    nodes = nodes_list(case_study)
    # Write nodes to topology
    topology['nodes'] = nodes

    # Get carriers list
    carriers = carriers_list(case_study)
    # Write carriers to topology
    topology['carriers'] = carriers

    # Get periods list
    periods = periods_list(case_study)
    # Write periods to topology
    topology['investment_periods'] = periods
    topology['start_date'] = f'{periods[0]}-01-01 00:00'
    topology['end_date'] = f'{periods[0]}-12-31 23:00'

    topology['resolution'] = resolution(case_study)

    # Save topology file
    topology_path.write_text(json.dumps(topology, indent=2))

    return



def nodes_list(case_study: Path | str):
    '''
    Take nodes list from plants_clusters_summary.csv
    In case, select a subset of nodes for the example
    '''
    
    # all nodes df upload
    nodes_df = pd.read_csv(f"case_studies/{case_study}/plants_clusters_summary.csv")

    # Create nodes list from dataframe
    nodes = nodes_df['cluster'].tolist()

    return nodes


def carriers_list(case_study: Path | str):
    '''
    Define carriers list
    '''
    carriers = pd.read_excel(f"case_studies/{case_study}/carriers_list.xlsx")['CARRIERS'].tolist()
    
    return carriers


def periods_list(case_study: Path | str):
    '''
    Define periods list
    '''
    # Determine period from case study name
    map = {
        "current_layout": "2020",
        "current_layout_optimal": "2025",
        "2030": "2030",
        "2040": "2040",
        "2050": "2050"
    }

    if case_study not in map:
        raise ValueError(f"Unexpected case study name: {case_study}. Cannot determine period.")
    
    periods = [map[case_study]]
    
    return periods

def resolution(case_study: Path | str):
    '''
    Define resolution for the model
    '''
    time_index = pd.read_excel(f"case_studies/{case_study}/carriers/electricity.xlsx")['datetime'].tolist()
    n_h = len(time_index)

    if n_h == 8760:
        resolution = '1h'  # hourly
    elif n_h == 8760/2:
        resolution = '2h'  # 2-hourly
    elif n_h == 8760/3:
        resolution = '3h'  # 3-hourly
    elif n_h == 8760/4:
        resolution = '4h'  # 4-hourly
    else:
        raise ValueError(f"Unexpected number of time steps: {n_h}. Cannot determine resolution.")

    return resolution