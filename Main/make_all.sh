#!/usr/bin/bash

sudo hciconfig hci0 piscan
sudo chmod o+rw /var/run/sdp
make
python3 py/Setup.py
sudo i2cdetect -y 1
