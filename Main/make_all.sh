#!/usr/bin/bash

make
python3 py/Setup.py
sudo i2cdetect -y 1
