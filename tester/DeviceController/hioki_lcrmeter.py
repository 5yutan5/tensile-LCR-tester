import time
from typing import Union

from serial import Serial

DISPLAY = {True: ":DISP ON", False: ":DISP OFF"}
MEASURE_OUTPUT_AUTO = {True: ":MEAS:OUTP:AUTO ON", False: "MEAS:OUTP:AUTO OFF"}
MODE = {"LCR": ":MODE LCR", "CONTINUOUS": ":MODE CONT"}
SPEED = {
    "FAST": ":SPEE FAST",
    "MEDIUM": ":SPEE MED",
    "SLOW": ":SPEE SLOW",
    "SLOW2": ":SPEE SLOW2",
}
TRIGGER_EXTERNAL = {True: ":TRIG EXT", False: ":TRIG INT"}
PARAMETER = parameters = {
    "None": None,
    "Z    (Impedance)": "Z",
    "Y    (Admittance)": "Y",
    "θ    (Phase angle)": "θ",
    "X    (Reactance)": "X",
    "G    (Conductance)": "G",
    "B    (Susceptance)": "B",
    "Q    (Q-factor)": "Q",
    "Rdc  (DC resistance)": "Rdc",
    "Rs   (Equivalent series resistance)": "Rs",
    "Rp   (Equivalent parallel resistance)": "Rp",
    "Ls   (Equivalent series inductance)": "Ls",
    "Lp   (Equivalent parallel inductance)": "Lp",
    "Cs   (Equivalent series Capacitance)": "Cs",
    "Cp   (Equivalent parallel capacitance)": "Cp",
    "D    (Loss factor tanδ)": "D",
    "σ    (Conductivity)": "σ",
    "ε    (Permittivity)": "ε",
}


class LCRMeterTimeoutError(Exception):
    pass


class LCRMeterSerial(Serial):
    def __init__(self) -> None:
        super().__init__(timeout=0)
        self._delimiter = "\r\n"

    def send_message(self, message: str) -> None:
        self.write(bytes(message + self._delimiter, "utf-8"))

    def receive_message(self, timeout: int) -> str:
        start = time.time()
        responses = bytes()
        while True:
            if self.in_waiting > 0:
                response = self.read(1)
                if response == b"\n":
                    break
                elif response == b"\r":
                    pass
                else:
                    responses += response

            if time.time() - start > timeout:
                raise LCRMeterTimeoutError()
        return responses.decode("utf-8")

    def send_query_message(self, message: str, timeout: int) -> str:
        self.send_message(message)
        return self.receive_message(timeout)


class LCRMeterIM3536:
    PORT_FILTER = ""
    BAUDRATES = ["9600", "19200", "38400", "57600"]

    def __init__(self) -> None:
        self._ser = LCRMeterSerial()
        self._timeout = int()
        self.measure_output_auto = False

    def open(self, port: Union[str, None], baudrate: Union[int, None]) -> None:
        self._ser.port = port
        self._ser.baudrate = baudrate
        self._ser.open()

    def close(self) -> None:
        self._ser.close()

    def set_options(
        self, timeout: int, display_monitor: bool, measure_output_auto: bool, speed: str
    ) -> None:
        self.measure_output_auto = measure_output_auto
        self._timeout = timeout
        self.set_enable_display_monitor(display_monitor)
        self.set_enable_measure_output_auto(measure_output_auto)
        self.set_speed(speed)

    def set_parameters(
        self, param1: str, param2: str = None, param3: str = None, param4: str = None
    ) -> None:
        self._ser.send_message(f":PARameter1 {param1}")
        if param2 is not None:
            self._ser.send_message(f":PARameter2 {param2}")
        if param3 is not None:
            self._ser.send_message(f":PARameter3 {param3}")
        if param4 is not None:
            self._ser.send_message(f":PARameter4 {param4}")

    def trigger(self) -> Union[str, None]:
        if self.measure_output_auto:
            return self._ser.send_query_message("*TRG", self._timeout)
        else:
            self._ser.send_message("*TRG")

    def reset_current_settings(self) -> None:
        self._ser.send_message(":PRESet")

    def reset_all(self) -> None:
        self._ser.send_message("*RST")

    def get_monitor_values(self) -> str:
        return self._ser.send_query_message(":Monitor?", self._timeout)

    def set_enable_trigger_external(self, is_enable: bool) -> None:
        self._ser.send_message(TRIGGER_EXTERNAL[is_enable])

    def set_mode(self, mode: str) -> None:
        self._ser.send_message(MODE[mode])

    def set_enable_measure_output_auto(self, is_enable: bool) -> None:
        self._ser.send_message(MEASURE_OUTPUT_AUTO[is_enable])

    def set_enable_display_monitor(self, is_enable: bool) -> None:
        self._ser.send_message(DISPLAY[is_enable])

    def set_speed(self, mode: str) -> None:
        self._ser.send_message(SPEED[mode])
