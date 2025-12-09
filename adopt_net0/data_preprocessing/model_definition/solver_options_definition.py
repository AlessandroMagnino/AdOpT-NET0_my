from pathlib import Path
import pandas as pd
import json

def solver_options_definition(input_path: Path |str):
    '''
    Fill ConfigModel.json with solver options
    '''

    config_path = Path(input_path) / "ConfigModel.json"
    config = json.loads(config_path.read_text())

    solver = 'gurobi'
    MIPGap = 1 # %
    time_lim = 24*30 # hours

    config['solveroptions']['solver']['value'] = solver
    config['solveroptions']['mipgap']['value'] = MIPGap / 100  # Convert percentage to fraction
    config['solveroptions']['timelim']['value'] = time_lim

    # Save config file
    config_path.write_text(json.dumps(config, indent=2))
    
    return

