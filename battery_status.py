import datetime
import logging
import queue
import signal
import tkinter as tk
from tkinter import ttk
import time
import threading

from INA219 import INA219

logging.basicConfig(level=logging.INFO)


class TimeoutException(Exception):  # Custom exception class
    pass


def timeout_handler(signum, frame):  # Custom signal handler
    raise TimeoutException


# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)


class BatteryStatus:
    __slots__ = ['root', 'table', 'queue', 'update_interval']

    def __init__(self, update_interval=60):
        self.root = tk.Tk()
        self.root.title("Battery Status")

        self.table = ttk.Treeview(self.root, columns=('Parameter', 'Value'), show='headings')
        self.table.grid(row=0, column=0, sticky='nsew')  # Place the table at the top of the window
        for col in ('Parameter', 'Value'):
            self.table.heading(col, text=col)

        self.queue = queue.Queue()
        self.update_interval = update_interval  # update interval in seconds

    def update_status(self):
        """Update the battery status."""
        while True:
            try:
                # Set the signal to trigger after 5 seconds
                signal.alarm(5)
                ina219 = INA219(addr=0x42)

                bus_voltage = ina219.getBusVoltage_V()
                current = ina219.getCurrent_mA()
                power = ina219.getPower_W()
                p = (bus_voltage - 6) / 2.4 * 100
                if (p > 100): p = 100
                if (p < 0): p = 0

                # Get the current time
                now = datetime.datetime.now()
                # Format the time as a string
                now_str = now.strftime("%Y-%m-%d %H:%M:%S")

                # Put the data into the queue
                self.queue.put((bus_voltage, current, power, p, now_str))

                # Reset the alarm
                signal.alarm(0)

                # Append the battery status to the log file
                with open('battery_status.log', 'a') as f:
                    if current < 0:
                        f.write(f"{now_str} - Percent {p}, Battery is discharging\n")
                    else:
                        f.write(f"{now_str} - Percent {p}, Battery is charging\n")

            except TimeoutException:
                logging.error('Function call timed out')

            # Sleep for the update interval
            time.sleep(self.update_interval)

    def update_gui(self):
        """Update the GUI with the data from the queue."""
        try:
            # Get the data from the queue
            bus_voltage, current, power, p, now_str = self.queue.get_nowait()

            # Clear the table
            for row in self.table.get_children():
                self.table.delete(row)

            # Insert the data into the table
            # self.table.insert('', 'end', values=("Voltage", f"{bus_voltage:.3f} V"))
            # self.table.insert('', 'end', values=("Current", f"{current / 1000:.6f} A"))
            # self.table.insert('', 'end', values=("Power", f"{power:.3f} W"))
            self.table.insert('', 'end', values=("Percent", f"{p:.1f}%"))
            if current < 0:
                self.table.insert('', 'end', values=("Battery", "Battery is discharging"))
            else:
                self.table.insert('', 'end', values=("Battery", "Battery is charging"))

            self.table.insert('', 'end', values=("Last Updated", now_str))

        except queue.Empty:
            pass

        # Schedule the next update
        self.root.after(300, self.update_gui)

    def run(self):
        """Start the Tkinter event loop."""
        threading.Thread(target=self.update_status, daemon=True).start()
        self.update_gui()
        self.root.mainloop()


if __name__ == "__main__":
    logging.info("Starting Battery Status application.")
    app = BatteryStatus()
    app.run()
