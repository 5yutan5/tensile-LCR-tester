from dataclasses import dataclass
from typing import Union


@dataclass
class DeviceStatus:
    baudrate: Union[int, None] = None
    description: Union[str, None] = None
    is_connecting: bool = False
    port: Union[str, None] = None
