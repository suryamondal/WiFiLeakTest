----------------------------------------------------------------------

# Wireless Leak Test — NodeMCU / BMP180

This directory contains the firmware and helper scripts used to program
NodeMCU (ESP8266) boards that read BMP180 pressure/temperature sensors
and transmit the data over UDP to the backend.

The same firmware is used for every station. Station-specific
configuration (station number, WiFi credentials, backend IP) is
provided through command-line options at upload time — no manual
edits to the source code are required.

Hardware
--------

| Component         | Notes                                |
|-------------------|--------------------------------------|
| NodeMCU v1.0      | ESP8266-based Wi-Fi board            |
| BMP180 breakout   | Pressure + temperature sensor (I²C)  |

Wiring (BMP180 → NodeMCU)
--------------------------

| BMP180 | NodeMCU |
|--------|---------|
| VIN    | 3.3V    |
| GND    | GND     |
| SCL    | D5      |
| SDA    | D4      |

If D4 or D5 are unavailable, use any free digital pins and update
`Wire.begin(D4, D5)` in the Adafruit BMP085 library source
(`~/.arduino15/...` or `~/Arduino/libraries/Adafruit_BMP085_Library/`)
accordingly.

Station Numbering
-----------------

| Station | Role                                      |
|---------|-------------------------------------------|
| 0       | Atmosphere reference (ambient pressure)   |
| 1 .. N  | Each RPC gap under test                   |

No two NodeMCUs may share the same station number during a test run.
At least two units are needed: one station-0 atmosphere reference
and one or more RPC gap stations.

Install arduino-cli
-------------------

```BASH
# Remove snap-installed versions if present
sudo snap remove arduino-cli
sudo snap remove curl
# Install curl and arduino-cli
sudo apt install curl
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
sudo mv bin/arduino-cli /usr/local/bin/
# Verify installation
arduino-cli version
# Increase download timeout (ESP8266 core is large)
arduino-cli config set network.connection_timeout 1200s
# Register the ESP8266 board URL in config (skip if already present)
arduino-cli config dump | grep -q "arduino.esp8266.com" || \
    arduino-cli config add board_manager.additional_urls \
        http://arduino.esp8266.com/stable/package_esp8266com_index.json
# Fetch package index and install ESP8266 core
arduino-cli core update-index
arduino-cli core install esp8266:esp8266
# Check installed cores
arduino-cli core list
# Install required libraries
arduino-cli lib install "Adafruit BMP085 Library"
# (Wire, ESP8266WiFi, WiFiUdp are built into the ESP8266 core — no separate install needed)
```

Run / Upload
------------

```BASH
# Show help
python3 upload-nodemcu.py -h

# Upload station 0 (atmosphere reference)
python3 upload-nodemcu.py \
    --station 0 \
    --ssids "iichep1_ng,iichep2_ng,iichep3_ng" \
    --passwords "pass1,pass2,pass3" \
    --ip 192.168.183.121

# Upload station 2 (RPC gap #2) on a specific serial port
python3 upload-nodemcu.py \
    --station 2 \
    --ssids "iichep1_ng,iichep2_ng,iichep3_ng" \
    --passwords "pass1,pass2,pass3" \
    --ip 192.168.183.121 \
    --port /dev/ttyACM0

# Compile only, no upload
python3 upload-nodemcu.py \
    --station 1 \
    --ssids "net" --passwords "pass" \
    --ip 192.168.1.100 \
    --build-only
```

Permission Problems
-------------------

```BASH
sudo usermod -aG dialout $USER
# then logout/login for it to take effect
```

Find the Serial Port
--------------------

```BASH
ls /dev/tty*
# plug in the NodeMCU and re-run to see which entry appears — usually
# /dev/ttyUSB0 or /dev/ttyACM0
```

Monitor Serial Output
---------------------

```BASH
arduino-cli monitor -p /dev/ttyUSB0 -c baudrate=9600
```

Reference
---------

The theory and methodology behind this wireless leak test setup are
described in the following publications:

- [Preprint (arXiv:1812.00277)](https://arxiv.org/abs/1812.00277)
- [Published — JINST 14 P04009 (2019)](https://doi.org/10.1088/1748-0221/14/04/P04009)

----------------------------------------------------------------------

UDP Packet Format
----------------------------------------------------------------------

Each NodeMCU transmits a UDP packet every `--display-interval` seconds
(default 3 s) to the configured backend IP on port 5006:

```
<station_id> <temperature_°C> <pressure_Pa>
```

Example output from station 2:

```
2 24.50 101325.0
```

The backend scripts in `Code_Madurai_NodeMCU/bin/` handle the data:

```BASH
cd Code_Madurai_NodeMCU/bin

# Start the UDP receiver (leave running for the full test)
./receiveUDP.py

# Register an RPC gap for logging (in a separate terminal)
# Format: <station_no> <RPC_name> <run_number> <pressure_offset>
python3 RPC_Names.py

# Live pressure-difference display for a specific station
./RPC_Display.py <Station No> &
```

`receiveUDP.py` logs packets from all stations to `Code_Madurai_NodeMCU/data/`.
Pressure difference between any RPC station and station 0 (atmosphere)
indicates a leak or pop-up event at that gap.

---------------------------------------
