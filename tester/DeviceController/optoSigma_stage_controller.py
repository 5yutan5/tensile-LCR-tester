from dataclasses import dataclass
from enum import Enum
from typing import Union

from serial import Serial
from serial.serialutil import EIGHTBITS, PARITY_NONE, STOPBITS_ONE


class StageControllerSerial(Serial):
    def __init__(self):
        super().__init__(timeout=0)
        self._delimiter = b"\r\n"

    def send_message(self, message: str) -> None:
        self.write(message.encode("ascii") + self._delimiter)

    def recieve_message(self) -> str:
        response = (self.readline()[: -1 * len(self._delimiter)]).decode("utf-8")
        return response

    def send_query_message(self, message: str) -> str:
        self.send_message(message)
        return self.recieve_message()


@dataclass
class StageSGSP26_200:
    X_MICRO_PER_PULSE_FULL: int = 4
    division: int = 4
    x_micro_per_pulse: int = int(X_MICRO_PER_PULSE_FULL / division)


class StageControllerShot702:
    class DirectionMode(Enum):
        PLUS = "+"
        MINUS = "-"

    class MoveMode(Enum):
        ABSOLUTE = "A:1"
        RELATIVE = "M:1"

    class SpeedMode(Enum):
        MOVE = "D:1"
        RETURN_ORIGIN = "V:1"

    PORT_FILTER = "ATEN"

    def __init__(self) -> None:
        self._ser = StageControllerSerial()
        self._stage = StageSGSP26_200()
        self._timeout = 10

    def open(self, port: Union[str, None]) -> None:
        self._ser.port = port
        self._ser.baudrate = 38400
        self._ser.bytesize = EIGHTBITS
        self._ser.stopbits = STOPBITS_ONE
        self._ser.timeout = 1
        self._ser.parity = PARITY_NONE
        self._ser.rtscts = True
        self._ser.open()

    def close(self) -> None:
        self._ser.close()

    def initialize(self) -> None:
        self._set_division(self._stage.division)

    def _get_division(self) -> int:
        return int(self._ser.send_query_message("?:S1"))

    def _get_status(self) -> list[str]:
        return self._ser.send_query_message("Q:").split(",")

    def get_speed(self) -> str:
        return self._ser.send_query_message("?:D1")

    def get_position(self) -> int:
        position_pulse = self._get_status()[0].replace(" ", "")
        return int(position_pulse) * self._stage.x_micro_per_pulse

    def is_busy(self) -> bool:
        return self._ser.send_query_message("!:") == "B"

    def is_ready(self) -> bool:
        return self._ser.send_query_message("!:") == "R"

    def _speed_to_pulse(self, s_micro: int) -> int:
        return int(s_micro / self._stage.x_micro_per_pulse)

    def set_stage_speed(
        self,
        min_micro,
        max_micro,
        acceleration_time_milli,
        mode: SpeedMode = SpeedMode.MOVE,
    ) -> None:
        min_pulse = self._speed_to_pulse(min_micro)
        max_pulse = self._speed_to_pulse(max_micro)
        command = f"{mode.value}S{min_pulse}F{max_pulse}R{acceleration_time_milli}"
        self._ser.send_query_message(command)

    def _set_division(self, division: int) -> None:
        self._ser.send_query_message(f"S:1{division}")

    def _drive_stage(self) -> None:
        self._ser.send_query_message("G:")

    def fix_zero(self) -> None:
        self._ser.send_query_message("R:1")

    @staticmethod
    def _check_direction(value) -> str:
        return "-" if value < 0 else "+"

    def move_stage(self, x_micro: int, mode: MoveMode = MoveMode.ABSOLUTE) -> None:
        direction = self._check_direction(x_micro)
        pulse = int(x_micro / self._stage.x_micro_per_pulse)
        command = f"{mode.value}{direction}P{abs(pulse)}"
        self._ser.send_query_message(command)
        self._drive_stage()

    def move_stage_to_zero(self) -> None:
        self._ser.send_query_message("H:1")

    def stop(self) -> None:
        self._ser.send_query_message("L:1")

    def emergency_stop(self) -> None:
        self._ser.send_query_message("L:E")

    def jog(self, direction: DirectionMode) -> None:
        self._ser.send_query_message(f"J:1{direction.value}")
        self._drive_stage()


def test():
    stage_controller = StageControllerShot702()
    stage_controller.open("COM6")
    stage_controller.initialize()
    print(stage_controller.get_position())
    stage_controller.set_stage_speed(10000, 10000, 100, stage_controller.SpeedMode.MOVE)
    stage_controller.fix_zero()
    stage_controller.move_stage(-10000)


def test_origin():
    stage_controller = StageControllerShot702()
    stage_controller.open("COM6")


if __name__ == "__main__":
    test()
