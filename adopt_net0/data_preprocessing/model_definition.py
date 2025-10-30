import pandas as pd
import json

def topology_definition(input_path):
    # Define the network topology here
    
    topology_path = f"{input_path}/Topology.json"

    topology = json.loads((topology_path).read_text())
    