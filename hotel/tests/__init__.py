import json
import os


def load_api_fixture(filename: str, as_string=False):
    base_dir = os.path.realpath(os.path.dirname(__file__))

    if filename.endswith(".json"):
        with open(f"{base_dir}/api_fixtures/{filename}") as f:
            if as_string:
                return f.read()

            return json.load(f)
    else:
        return open(f"{base_dir}/api_fixtures/{filename}").read()
