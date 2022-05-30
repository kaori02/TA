# - Init condition:
#   - 2 LiDAR tersambung, 1 LiDAR nyambung ke pin tertentu dengan kabel orange.
# - Matiin dlu si LiDAR via kabel orange.
# - Set alamat buat yg ga pake kabel orange ke `0x44`. RUN LiDAR ini
# - Turn on lagi kabel orange (dia bakal pake addr default `0x62`). RUN
# - Done
import RPi.GPIO as GPIO
import subprocess
import time

LedPin = 22         # pin11 
def GpioSetup():      
  GPIO.setmode(GPIO.BOARD)        # Set the board mode  to numbers pins by physical location
  GPIO.setup(LedPin, GPIO.OUT)    # Set pin mode as output
  GPIO.output(LedPin, GPIO.LOW)   # Set pin to high(+3.3V) to off the led
  time.sleep(1.0)                 # wait 1 sec
  
  # disini pindahin alamat yang on ke 44
  moveOutput = subprocess.run(["../bin/moveTo0x44.out"])
  print("The exit code was: %d" % moveOutput.returncode)
  
  # nyala lagi
  GPIO.output(LedPin, GPIO.HIGH)   # led on

def GpioEndSetup():
  GPIO.cleanup()

if __name__ == '__main__':
  GpioSetup()
  GpioEndSetup()