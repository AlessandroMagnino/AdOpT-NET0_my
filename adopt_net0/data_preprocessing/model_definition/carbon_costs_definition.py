from pathlib import Path
import pandas as pd
import json

def carbon_costs_definition(case_study: Path | str,
                            input_path: Path | str):
    '''
    Define carbon costs data file
    '''

    # Topology, nodes and periods
    topology_path = Path(input_path) / "Topology.json"
    topology = json.loads(topology_path.read_text())
    nodes = topology['nodes']
    periods = topology['investment_periods']

    for period in periods:
        for node in nodes:
            # Open carbon costs data file
            carbon_costs_file_path = Path('case_studies') / case_study / 'carriers' / f"carbon_costs.xlsx"
            carbon_costs_data = pd.read_excel(carbon_costs_file_path, sheet_name=node, index_col=0)
            # convert index to datetime
            carbon_costs_data.index = pd.to_datetime(carbon_costs_data.index)
            # remove 29th Feb if present
            carbon_costs_data = carbon_costs_data[~((carbon_costs_data.index.month == 2) & (carbon_costs_data.index.day == 29))]
            
            # CSV path
            output_csv_path = Path(input_path) / f"{period}/node_data/{node}/CarbonCost.csv"
            output_df = pd.read_csv(output_csv_path, index_col=0, sep=';')

            # Fill df
            output_df['price'] = carbon_costs_data['price'].values if 'price' in carbon_costs_data.columns else 0
            output_df['subsidy'] = carbon_costs_data['subsidy'].values if 'subsidy' in carbon_costs_data.columns else 0
            
            # Save csv
            output_df.to_csv(output_csv_path, sep=';')

    return
    