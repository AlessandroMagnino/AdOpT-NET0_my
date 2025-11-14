from pathlib import Path
import pandas as pd
import json

def carrier_data_definition(input_path: Path | str):
    '''
    Define carrier data files
    '''

    # Topology, nodes and periods
    topology_path = Path(input_path) / "Topology.json"
    topology = json.loads(topology_path.read_text())
    nodes = topology['nodes']
    periods = topology['investment_periods']
    carriers = topology['carriers']

    carrier_data = {}

    for period in periods:
        for node in nodes:
            for carrier in carriers:
                # Open carrier data file
                carrier_file_path = Path('plants_data') / f"{carrier}.xlsx"
                carrier_data = pd.read_excel(carrier_file_path, sheet_name=node, index_col=0)
                # convert index to datetime
                carrier_data.index = pd.to_datetime(carrier_data.index)
                # remove 29th Feb if present
                carrier_data = carrier_data[~((carrier_data.index.month == 2) & (carrier_data.index.day == 29))]
                
                # CSV path
                output_csv_path = Path(input_path) / f"{period}/node_data/{node}/carrier_data/{carrier}.csv"
                output_df = pd.read_csv(output_csv_path, index_col=0)

                # Fill df
                output_df['Demand'] = carrier_data['demand'].values
                output_df['Import limit'] = carrier_data['import_limit'].values
                output_df['Export limit'] = carrier_data['export_limit'].values
                output_df['Import price'] = carrier_data['import_price'].values
                output_df['Export price'] = carrier_data['export_price'].values
                
                # Save csv
                output_df.to_csv(output_csv_path)

    return