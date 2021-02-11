# tensile-LCR-tester
This application controls Hioki's LCR meter (IM3536) and Sigma Kouki's stage controller (controller: shot-702, stage: SGSP-26-200) at the same time.

This module is currently in production.

## Runtime Dependencies

**Important Note**: Most all of the dependencies listed below will not be installed automatically. So you need to install them.

- Python 3.9+
- PyQt5 5.9+
- psutil 5.8+
- pyserial 3.5+
- qdarkstyle
- qtpy
- 5yutan5/AutoLab
- 5yutan5/DeviceController

## Installation

It can be installed with both pip and conda, but installing with conda is deprecated.

### Use conda

```
pip install git+https://github.com/5yutan5/AutoLab
pip install git+https://github.com/5yutan5/DeviceController
pip install git+https://github.com/5yutan5/tensile-LCR-tester
```
and
```
conda install pyqt psutil pyserial qtpy qdarkstyle
```

### Use pip

```
pip install git+https://github.com/5yutan5/AutoLab
pip install git+https://github.com/5yutan5/DeviceController
pip install git+https://github.com/5yutan5/tensile-LCR-tester
```
and
```
pip install pyqt5 psutil pyserial qtpy qdarkstyle
```
