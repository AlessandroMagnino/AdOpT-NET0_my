from pathlib import Path
import json

def optimization_options_definition(input_path: Path |str):
    '''
    Fill ConfigModel.json with optimization options
    '''

    config_path = Path(input_path) / "ConfigModel.json"
    config = json.loads(config_path.read_text())

    objective = 'emissions_net' # costs, emissions_pos, emissions_net, emissions_minC, costs_emissionlimit, pareto
    # emission_limit = 0 # t total, only relevant if objective is 'costs_emissionlimit'

    typical_days = 5
    typical_days_method = 1

    # Set objective function
    config['optimization']['objective']['value'] = objective
    # config['optimization']['emission_limit']['value'] = emission_limit


    # Set optimization options
    config['optimization']['typicaldays']['N']['value'] = typical_days
    config['optimization']['typicaldays']['method']['value'] = typical_days_method

    # Save config file
    config_path.write_text(json.dumps(config, indent=2))

    return
