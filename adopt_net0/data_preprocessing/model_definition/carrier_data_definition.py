from pathlib import Path
import pandas as pd
import json

def carrier_data_definition(case_study: Path | str,
                            input_path: Path | str):
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
                carrier_file_path = Path('case_studies') / case_study / 'carriers' / f"{carrier}.xlsx"
                carrier_data = pd.read_excel(carrier_file_path, sheet_name=node, index_col=0)
                # convert index to datetime
                carrier_data.index = pd.to_datetime(carrier_data.index)
                # remove 29th Feb if present
                carrier_data = carrier_data[~((carrier_data.index.month == 2) & (carrier_data.index.day == 29))]
                
                # CSV path
                output_csv_path = Path(input_path) / f"{period}/node_data/{node}/carrier_data/{carrier}.csv"
                output_df = pd.read_csv(output_csv_path, index_col=0, sep=';')

                # Fill df
                output_df['Demand'] = carrier_data['demand'].values if 'demand' in carrier_data.columns else 0
                output_df['Import limit'] = carrier_data['import_limit'].values if 'import_limit' in carrier_data.columns else 0
                output_df['Export limit'] = carrier_data['export_limit'].values if 'export_limit' in carrier_data.columns else 1e6
                output_df['Import price'] = carrier_data['import_price'].values if 'import_price' in carrier_data.columns else 0
                output_df['Export price'] = carrier_data['export_price'].values if 'export_price' in carrier_data.columns else 0
                output_df['Import emission factor'] = carrier_data['import_emission_factor'].values if 'import_emission_factor' in carrier_data.columns else 0
                output_df['Export emission factor'] = carrier_data['export_emission_factor'].values if 'export_emission_factor' in carrier_data.columns else 0
                output_df['Generic production'] = carrier_data['generic_production'].values if 'generic_production' in carrier_data.columns else 0
                
                # Save csv
                output_df.to_csv(output_csv_path, sep=';')

    return