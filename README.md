# Battery Status GUI Application

This is a simple GUI application for Raspberry Pi that displays the battery status. It uses the INA219 sensor to measure the battery voltage, current, power, and percentage. The application is written in Python and uses the Tkinter library for the GUI.

## Dependencies

- Python 3
- Tkinter
- smbus
- **INA219.py** library (included in this repository)

## Installation

1. Ensure Python 3 is installed on your system. You can download it from the official [Python website](https://www.python.org/downloads/).

2. Install the smbus library using pip:

```bash
pip install smbus
```

## Usage
Run the script using Python:

```bash
python3 battary_status.py
```

**Note: Tested on [Waveshare UPS HAT B](https://www.waveshare.com/wiki/UPS_HAT_(B)#Document)** 
