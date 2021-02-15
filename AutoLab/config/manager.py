import json
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from typing import Any


def read_json(file_name: str) -> dict:
    json_data = {}
    try:
        f = open(file_name)
        json_data = json.load(f)
    except JSONDecodeError:
        return {}
    except IOError as e:
        print(e)
    return json_data


def to_json(file_name: str, data: dict) -> None:
    try:
        f = open(file_name, mode="w")
        json.dump(data, f)
    except IOError as e:
        print(e)


def extraction_settings(settings: dict[str, Any], target: str):
    return {key: item for key, item in settings.items() if target in key}


def merge_settings(default_settings, user_settings) -> dict[str, Any]:
    return default_settings | user_settings


def test():
    settings = get_settings()
    print(settings.stage_controller.minimum_speed)


if __name__ == "__main__":
    test()
