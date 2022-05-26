# kode yang dirun pas pertama nyalain LiDAR

import RPi.GPIO  as  GPIO
import  time

LedPin = 22         # pin11 
def setup():      
  GPIO.setmode(GPIO.BOARD)       # Set the board mode  to numbers pins by physical location
  GPIO.setup(LedPin, GPIO.OUT)   # Set pin mode as output
  GPIO.output(LedPin, GPIO.HIGH) # Set pin to high(+3.3V) to off the led
  GPIO.setup(13,GPIO.OUT)

def loop():     
  while True:            
         GPIO.output(LedPin, GPIO.LOW)   # led on
         time.sleep(1.0)                                  # wait 1 sec    
         GPIO.output(LedPin, GPIO.HIGH)  # led off
         time.sleep(1.0)                                  # wait 1 sec
def destroy():
        GPIO.output(LedPin, GPIO.HIGH)     # led off
        GPIO.cleanup()                                    # Release resource

if __name__ == '__main__':                  # Program start from here
      setup()
      try:
              loop()
      except KeyboardInterrupt:            # When 'Ctrl+C' is pressed, the destroy() will be  executed.
              destroy