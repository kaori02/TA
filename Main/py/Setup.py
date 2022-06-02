import RPi.GPIO as GPIO
import subprocess
import time

LedPin = 22
def GpioSetup():      
  GPIO.setmode(GPIO.BOARD)        # Set the board mode  to numbers pins by physical location
  GPIO.setup(LedPin, GPIO.OUT)    # Set pin mode as output
  GPIO.output(LedPin, GPIO.LOW)   # off
  time.sleep(1.0)                 # wait 1 sec
  
  # disini pindahin alamat yang on ke 44
  moveOutput = subprocess.run(["bin/moveTo0x44.out"])
  print("The exit code was: %d" % moveOutput.returncode)
  
  # nyala lagi
  GPIO.output(LedPin, GPIO.HIGH)   # on

def GpioEndSetup():
  GPIO.cleanup()

if __name__ == '__main__':
  GpioSetup()
  GpioEndSetup()
