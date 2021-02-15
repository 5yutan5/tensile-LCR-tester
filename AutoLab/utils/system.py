import psutil
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo


def phymem_usage() -> float:
    """
    Return physical memory usage (float)
    Requires the cross-platform psutil (>=v0.3) library
    (https://github.com/giampaolo/psutil)
    """
    return psutil.virtual_memory().percent


def cpu_usage():
    """
    Return CPU usage (float)
    Requires the cross-platform psutil (>=v0.3) library
    (https://github.com/giampaolo/psutil)
    """
    return psutil.cpu_percent(interval=0)


def search_ports(filter: str) -> list[ListPortInfo]:
    return [port for port in list_ports.comports() if filter in str(port.description)]


def test():
    print("*" * 80)
    print("Mem: ", phymem_usage())
    print("CPU: ", cpu_usage())
    print("*" * 80)


if __name__ == "__main__":
    test()
