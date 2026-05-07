from pathlib import Path
import json

def optimization_options_definition(case_study: str, input_path: Path |str):
    '''
    Fill ConfigModel.json with optimization options
    '''
    case_study_path = Path('case_studies') / case_study

    # open json file
    config_specs_path = case_study_path / "config_specs.json"
    config_specs = json.loads(config_specs_path.read_text())

    config_path = Path(input_path) / "ConfigModel.json"
    config = json.loads(config_path.read_text())

    # Set objective function
    config['optimization']['objective']['value'] = config_specs['optimization']['objective']['value']
    # Set emission limit if objective is costs_emissionlimit
    if config_specs['optimization']['objective']['value'] == 'costs_emissionlimit':
        config['optimization']['emission_limit']['value'] = config_specs['optimization']['emission_limit']['value']

    # Set optimization options
    config['optimization']['typicaldays']['N']['value'] = config_specs['optimization']['typicaldays']['N']['value']
    config['optimization']['typicaldays']['method']['value'] = config_specs['optimization']['typicaldays']['method']['value']

    config['solveroptions']['solver']['value'] = config_specs['solveroptions']['solver']['value']
    config['solveroptions']['mipgap']['value'] = config_specs['solveroptions']['mipgap']['value']
    config['solveroptions']['timelim']['value'] = config_specs['solveroptions']['timelim']['value']
    config['solveroptions']['method']['value'] = config_specs['solveroptions']['method']['value']
    # config['solveroptions']['NodeMethod']['value'] = config_specs['solveroptions']['NodeMethod']['value']

    config['scaling']['scaling_on']['value'] = config_specs['scaling']['scaling_on']['value']
    config['scaling']['scaling_factors']['energy_vars']['value'] = config_specs['scaling']['scaling_factors']['energy_vars']['value']
    config['scaling']['scaling_factors']['cost_vars']['value'] = config_specs['scaling']['scaling_factors']['cost_vars']['value']
    config['scaling']['scaling_factors']['objective']['value'] = config_specs['scaling']['scaling_factors']['objective']['value']

    # Save config file
    config_path.write_text(json.dumps(config, indent=2))

    return
