# TA

Code for my Final Project

## How to connect wireless

- Check its ip (scan)
- Connect via vnc with the ip or via ssh like the following:

  ```sh
  ssh kaoripi@192.168.0.4
  ```

- Enter password

## Instructions to enable the I2C peripheral in the ARM core

```sh
sudo raspi-config
```

From the menu, select

- Interfacing Options
- P5 I2C
- Enable the interface
- Select Finish
- Reboot the Raspberry Pi

## Pin

```txt
* LLv3 Blue  (SDA) - RPi pin 3 (GPIO 2)
* LLv3 Green (SCL) - RPi pin 5 (GPIO 3)
* LLv3 Red   (5V ) - RPi pin 4
* LLv3 Black (GND) - RPi pin 6

- Wire a 680uF capacitor across pins 4 and 6
```

## How To Run

Check [README](Main/README.md) file in `Main` directory.