# Encoder Test Bench

## Directory Informaiton 
This project has two directories `python` and `src`.
- `python` has three files, of which two are intended to be used.
    - `com_ports.py` : Determines which COM ports are being used over Serial. It will print the detected COM port into the terminal.
    - `record.py` : Records the data received over serial. Before running you must set the correct COM port. This is set in line 22. When this code is run it will ask for what type of encoder is being used. You can type either Magnetic or Capacitive (or simply M or C) to select the correct type. The code defaults to capacitive. This being set rescales the graph to the maximum of each respective motor. It also changes the name of the csv file the data is saved to (either Magnetic_readings.csv or Capacitive_readings.csv). Subsequent runnings of the code of the same type of the encoder will OVERWRITE the existing file. It is recommended to save the csv to either another name of a different folder after recording data. The data saved has a timestamp in the s.ms format since epoch and the value read. 
    - `rendering.py` : Contains helper functions for liveplotting.
- `src` only contains the main file. It is not anticipated to be used.
    - `main.cpp` contains the code which reads the encoder over SPI. The encoder type must be set before flashing. It can be set on lines 3 or 4.

## Flashing The Code
The teensy 4.0s have pre-flashed code on them. There is not an anticipated need to re-flash them.However, if they must be reflashed the instructions are as follows.
- Open VSCode with the Platform IO Extension. If installing for the first time, you may have to restart VSCode.
- Select the extension then pick folder and select the folder with the .ini file
- Let the project configure
- At the bottom of VScode there will be a bar with several icons including Build, Upload, and Serial Monitor. 
- Click Upload and main.cpp will be compiled and uploaded.

## Running The Code
The instructions for running the code are as follows:
- Plug in the Teensy to a USB port on a monitoring computer, the code loaded onto it should start once power is received.
- Run `record.py` on the monitoring computer with the correct COM port set in the python file. 
- Select the encoder type.
- Provide power to the motor as fit.
- Everything should now be working. 

## Debug

### The Teensy Does Not Run Code
- Power cycle
- Re-flash code if power cycling is not correct
- Ensure flashed code is for the correct encoder type.

### The Encoder Output is Invalid / Does Not Change
- Ensure Teensy is running code for the correct Encoder
- Validate continunity of wires

### The Python File Does Work / Run
- Ensure the correct COM port is set
- Ensure nothing else is reading the same port (cannot have both using at the same time). Python should throw an error in this case.
- Ensure the Teensy is outputing over Serial. You can open a separate Serial Monitor in VScode to validate this. 
- Ensure you have all the correct python packages
    - pyserial
    - matplotlib
    - numpy

### Other
- If nothing else worked please contact me at lukebatteas2027@u.northwestern.edu