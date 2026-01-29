from pathlib import Path
import json

def optimization_options_definition(input_path: Path |str):
    '''
    Fill ConfigModel.json with optimization options
    '''

    config_path = Path(input_path) / "ConfigModel.json"
    config = json.loads(config_path.read_text())

    typical_days = 5
    typical_days_method = 1

    # Set optimization options
    config['optimization']['typicaldays']['N']['value'] = typical_days
    config['optimization']['typicaldays']['method']['value'] = typical_days_method

    # Save config file
    config_path.write_text(json.dumps(config, indent=2))

    return
