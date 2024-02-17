import tkinter as tk
from tkinter import ttk
from INA219 import INA219
import time
import logging
import threading

logging.basicConfig(level=logging.INFO)

class BatteryStatus:
    __slots__ = ['root', 'voltage_label', 'current_label', 'power_label', 'percent_label']

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Battery Status")

        self.voltage_label = ttk.Label(self.root, text="")
        self.voltage_label.pack()
        self.current_label = ttk.Label(self.root, text="")
        self.current_label.pack()
        self.power_label = ttk.Label(self.root, text="")
        self.power_label.pack()
        self.percent_label = ttk.Label(self.root, text="")
        self.percent_label.pack()

    def update_status(self):
        """Update the battery status."""
        while True:
            ina219 = INA219(addr=0x42)

            bus_voltage = ina219.getBusVoltage_V()
            current = ina219.getCurrent_mA()
            power = ina219.getPower_W()
            p = (bus_voltage - 6)/2.4*100
            if(p > 100):p = 100
            if(p < 0):p = 0

            self.voltage_label.config(text=f"Voltage: {bus_voltage:.3f} V")
            self.current_label.config(text=f"Current: {current/1000:.6f} A")
            self.power_label.config(text=f"Power: {power:.3f} W")
            self.percent_label.config(text=f"Percent: {p:.1f}%")

            # Update the status every 10 seconds.
            time.sleep(10)

    def run(self):
        """Start the Tkinter event loop."""
        threading.Thread(target=self.update_status, daemon=True).start()
        self.root.mainloop()

if __name__ == "__main__":
    logging.info("Starting Battery Status application.")
    app = BatteryStatus()
    app.run()