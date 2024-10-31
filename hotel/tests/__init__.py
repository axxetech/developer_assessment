import json
import os


def load_api_fixture(filename: str) -> str:
    base_dir = os.path.realpath(os.path.dirname(__file__))
    with open(f"{base_dir}/api_fixtures/{filename}") as f:
        return f.read()
