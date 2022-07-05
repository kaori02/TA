#!/usr/bin/bash

sudo hciconfig hci0 piscan
sudo chmod o+rw /var/run/sdp
python3 py/threading_Main.py
