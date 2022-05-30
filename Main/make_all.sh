#!/usr/bin/bash

make
python py/Setup.py
sudo i2cdetect -y 1
