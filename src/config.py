import yaml
import os
from pathlib import Path

def load_config()->dict:
    config_path = Path(__file__).parent.parent/"config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    config['storage']['password'] = os.getenv("POSTGRES_PASSWORD", config['storage'].get('password', ''))
    return config