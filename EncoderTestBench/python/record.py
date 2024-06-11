"""
Reads data from a serial port and displays it in real-time using matplotlib.
Make sure to set COM_PORT to the correct value before running.
"""

import serial
from rendering import PointsInSpace
from datetime import datetime
import csv



COM_PORT = "COM10"
TRAILING_POINTS = 100
MIN_MESSAGE_BYTES = 16

ser = serial.Serial(
    port=COM_PORT,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0,
)

print("Connected to: " + ser.portstr)

readings = []
timings = []

live_plotter = PointsInSpace(
                "Encoder Reading",
                "Reading",
                "Time Since Epoch [ms]",
                enable_grid=True,
                enable_legend=True,
               )

live_plotter.register_plot("Encoder Readings", alpha=1.0)
with open('recordings.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)

    while True:
        try:
            # Read bytes goofery
            bytes_to_read = ser.in_waiting
            if bytes_to_read < MIN_MESSAGE_BYTES:
                continue
            line = ser.read(bytes_to_read).decode("utf-8")
            segments = line.split()

            # Parse the message by reading the value after each label
            try:
                
                # Do this in two steps so that values are not changed if not all values exist
                def value_by_label(label):
                    return float(segments[segments.index(f"{label}:") + 1])

                reading = value_by_label("Encoder Reading:")
                time = datetime.now().time()

                readings.append(reading)
                timings.append(time)
                csv_writer.writerow(str(time) + ", " + str(reading))
            except Exception as e:
                print(e)
                continue

            if len(readings) > TRAILING_POINTS:
                readings.pop(0)
                timings.pop(0)
            # Display results
            live_plotter.start_drawing()
            live_plotter.draw_points("Encoder Readings", timings, readings)
            live_plotter.end_drawing()

        except Exception as e:
            print(e)
            ser.close()

    while True:
        try:
            # Read bytes goofery
            bytes_to_read = ser.in_waiting
            if bytes_to_read < MIN_MESSAGE_BYTES:
                continue
            line = ser.read(bytes_to_read).decode("utf-8")
            segments = line.split()

            # Parse the message by reading the value after each label
            try:
                
                # Do this in two steps so that values are not changed if not all values exist
                def value_by_label(label):
                    return float(segments[segments.index(f"{label}:") + 1])

                reading = value_by_label("Encoder Reading:")
                time = datetime.now().time()

                readings.append(reading)
                timings.append(time)
            except Exception as e:
                print(e)
                continue

            if len(readings) > TRAILING_POINTS:
                readings.pop(0)
                timings.pop(0)
            # Display results
            live_plotter.start_drawing()
            live_plotter.draw_points("Encoder Readings", timings, readings)
            live_plotter.end_drawing()

        except Exception as e:
            print(e)
            ser.close()
            print("Closed connection")
            quit()

    ser.close()
    print("Closed connection")

