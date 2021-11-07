import json
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from typing import Any

USER_FILE = "tester/config/user.json"

DEFAULT_SETTINGS = {
    "Console.maximumNumberOfLine": 200,
    "Main.measureInterval": 100,
    "LCRMeter.boadrate": 9600,
    "LCRMeter.communicationSpeed": "FAST",
    "LCRMeter.timeout": 5,
    "stageController.AccelerationandDecelerationTime": 10,
    "stageController.JudgeBusyInterval": 70,
    "stageController.MaximumSpeed": 10000,
    "stageController.MinimumSpeed": 500,
}


class Main:
    def __init__(self, settings) -> None:
        self.measure_interval: int = settings["Main.measureInterval"]


class LCRMeter:
    def __init__(self, settings) -> None:
        self.baudrate: int = settings["LCRMeter.boadrate"]
        self.communication_speed: str = settings["LCRMeter.communicationSpeed"]
        self.timeout: int = settings["LCRMeter.timeout"]


class StageController:
    def __init__(self, settings) -> None:
        self.acceleration_and_deceleration_time: int = settings["stageController.AccelerationandDecelerationTime"]
        self.judge_busy_interval: int = settings["stageController.JudgeBusyInterval"]
        self.maximum_speed: int = settings["stageController.MaximumSpeed"]
        self.minimum_speed: int = settings["stageController.MinimumSpeed"]


class Console:
    def __init__(self, settings) -> None:
        self.maximum_number_of_line = settings["Console.maximumNumberOfLine"]


@dataclass
class Settings:
    main: Main
    lcr_meter: LCRMeter
    stage_controller: StageController
    console: Console


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


def _extraction_settings(settings: dict[str, Any], target: str):
    return {key: item for key, item in settings.items() if target in key}


def _merge_settings(default_settings, user_settings) -> dict[str, Any]:
    return default_settings | user_settings


def get_settings() -> Settings:
    user_settings = read_json(USER_FILE)
    merge_settings = _merge_settings(DEFAULT_SETTINGS, user_settings)
    settings_main = Main(_extraction_settings(merge_settings, "Main"))
    settings_lcr_meter = LCRMeter(_extraction_settings(merge_settings, "LCRMeter"))
    settings_stage_controller = StageController(_extraction_settings(merge_settings, "stageController"))
    settings_console = Console(_extraction_settings(merge_settings, "Console"))
    return Settings(settings_main, settings_lcr_meter, settings_stage_controller, settings_console)


def test():
    settings = get_settings()
    print(settings.stage_controller.minimum_speed)


if __name__ == "__main__":
    test()
