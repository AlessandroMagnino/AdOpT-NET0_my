from pathlib import Path
import pandas as pd
import json

def technologies_definition(case_study: Path | str, input_path: Path | str):
    '''
    Fill for each node the Technologies.json file with existing and new technologies
    '''

    # Topology, nodes and periods
    topology_path = Path(input_path) / "Topology.json"
    topology = json.loads(topology_path.read_text())
    nodes = topology['nodes']
    periods = topology['investment_periods']

    # existing technologies file reading
    techs_file_path = Path("case_studies") / case_study / "technologies.xlsx"

    # Techs dataframes
    exist_techs_df = pd.read_excel(techs_file_path, sheet_name='existing', index_col=0)
    new_techs_df = pd.read_excel(techs_file_path, sheet_name='new', index_col=0)

    for period in periods:
        existing_by_node = existing_techs_map(exist_techs_df, nodes)
        new_by_node = new_techs_map(new_techs_df, nodes)

        for node in nodes:
            # Technologies.json file path
            techs_path = Path(input_path) / f"{period}" / "node_data" / node / "Technologies.json"
            technologies = json.loads(techs_path.read_text())
            technologies['existing'] = existing_by_node.get(node, {})
            technologies['new'] = new_by_node.get(node, [])

            techs_path.write_text(json.dumps(technologies, indent=4))

    return

    

def existing_techs_map(exist_techs_df: pd.DataFrame, nodes: list[str]):
    '''
    Get existing technologies for all nodes
    '''
    # Filter on nodes I am interested in
    exist_techs_df = exist_techs_df[exist_techs_df.index.isin(nodes)]

    # Clean columns names
    exist_techs_df.columns = [col.strip() for col in exist_techs_df.columns]
    exist_techs_map = exist_techs_df.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # remove zero columns
    non_zero_cols = exist_techs_map.columns[(exist_techs_map != 0).any()]
    exist_techs_map = exist_techs_map[non_zero_cols]

    # Create mapping per node
    techs_mapping = {
        node: exist_techs_map.loc[node][exist_techs_map.loc[node] > 0].to_dict()
        for node in exist_techs_map.index
    }
    
    return techs_mapping


def new_techs_map(new_techs_df: pd.DataFrame, nodes: list[str]):
    '''
    Get new technologies for all nodes
    '''

    # Filter on nodes I am interested in
    new_techs_df = new_techs_df[new_techs_df.index.isin(nodes)]

    # Clean columns names
    new_techs_df.columns = [col.strip() for col in new_techs_df.columns]
    new_techs_map = new_techs_df.apply(pd.to_numeric, errors='coerce').fillna(0)

    techs_mapping = {
        node: new_techs_map.columns[new_techs_map.loc[node] == 1].tolist()
        for node in new_techs_map.index
    }

    return techs_mapping


