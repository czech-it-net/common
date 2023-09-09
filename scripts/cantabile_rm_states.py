#!/bin/env python

# fix tempos: find . -type f -exec sed -i 's@"4/4"@"4\\/4"@' {} \;

import json
import logging
from pathlib import Path
from json.encoder import JSONEncoder

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def load_file(file_path):
    file_json = {}

    try:
        with open(file_path) as fhandle:
            file_json = json.load(fhandle)
            log.debug(f"Loaded: {file_path}")

    except json.decoder.JSONDecodeError:
        log.info(f"{file_path}: Skipping for JSON error")

    return file_json


def has_zero_states(file_json):
    return "states" in file_json and not len(file_json["states"])


def set_empty_routes_state_manager(file_json):
    changed = False

    for object in file_json["objects"]:
        for route in object.get("routes", []):
            if not route["stateManager"]["states"]:
                continue

            changed = True
            route["stateManager"] = {
                "behaviour": 1,
                "indexedBehaviour": None,
                "externalBehaviour": 0,
                "externalIndexedBehaviour": None,
                "nonLinkedBehaviour": 0,
                "nonLinkedIndexedBehaviour": None,
                "resetBehaviour": 0,
                "resetIndexedBehaviour": None,
                "states": {},
                "resetState": None
            }
    for note in file_json["showNotes"]:
        note["imageFile"] = ""
        note["imageFileRelative"] = ""

    return changed


def main():
    file_dir = Path(".")
    for file_path in file_dir.glob("*"):
        file_json = load_file(file_path)

        zero_states = has_zero_states(file_json)
        changed_route_states = set_empty_routes_state_manager(file_json)

        if zero_states and changed_route_states:
            with open(file_path, "w") as fhandle:
                log.info(f"{file_path}: Cleaning states")
                json.dump(file_json, fhandle, indent="\t")

        if not zero_states:
            log.warning(f"{file_path}: Skip - More states exist - NOT TREATED")
        elif not changed_route_states:
            log.info(f"{file_path}: Skip - No change needed")

if __name__ == "__main__":
    main()
