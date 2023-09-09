#!/bin/env python

import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def load_file(file_path):
    file_json = {}

    try:
        with open(file_path) as fhandle:
            file_json = json.load(fhandle)
            log.info(f"Loaded: {file_path}")

    except json.decoder.JSONDecodeError:
        log.warning(f"Skipping: {file_path} (JSON error)")

    return file_json


def has_zero_states(file_json):
    return "states" in file_json and len(file_json["states"])


def set_empty_routes_state_manager(file_json):
    for object in file_json["objects"]:
        for route in object.get("routes", []):
            del route["stateManager"]
            route["stateManager"] = {
                "behaviour": 1,
                "indexedBehaviour": null,
                "externalBehaviour": 0,
                "externalIndexedBehaviour": null,
                "nonLinkedBehaviour": 0,
                "nonLinkedIndexedBehaviour": null,
                "resetBehaviour": 0,
                "resetIndexedBehaviour": null,
                "states": {},
                "resetState": null
            }


def main():
    file_dir = Path(".")
    for file_path in file_dir.glob("*"):
        file_json = load_file(file_path)

        if has_zero_states(file_json):
            file_json["objects"][]

if __name__ == "__main__":
    main()
