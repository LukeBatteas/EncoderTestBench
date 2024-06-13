"""
Reads data from a serial port and displays it in real-time using matplotlib.
Make sure to set COM_PORT to the correct value before running.
"""

import serial
from rendering import PointsInSpace
import time
import csv
import sys

def main():
    
    print("Is Encoder Type Magnetic or Capacitive?")
    res = input()
    enc_type = 1
    enc_name = "Capacitive"
    if(res[0] == 'M'):
        enc_type = 0
        enc_name = "Magnetic"

    COM_PORT = '/dev/ttyACM0'
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

    max_val = 4096 
    if(not(enc_type)):
        max_val = 16384
    live_plotter = PointsInSpace(
                    enc_name + " Encoder Readings",
                    "Last 5 Seconds of Measurements[s]",
                    "Reading",
                    xlim=[0, 5],
                    ylim=[0, max_val],
                    enable_grid=True,
                    enable_legend=True,
                )

    live_plotter.register_plot("Encoder Readings", alpha=0.5)
    index = -1
    with open(enc_name + '_recordings.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["Time Since Epoch [s.ms]", "Encoder Reading"])

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
                        res = int(segments[segments.index(f"{label}:") + 1])
                        return res

                    reading = value_by_label("Reading")
                    time_ = time.time()

                    readings.append(reading)
                    timings.append(time_)
                    csv_writer.writerow([str(time_), str(reading)])
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

if __name__ == "__main__":
    main()