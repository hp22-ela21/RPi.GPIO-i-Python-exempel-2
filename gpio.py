#!/usr/bin/python3

################################################################################
# gpio.py: GPIO implementation of GPIO for Raspberry Pi in Python.
################################################################################
import RPi.GPIO as GPIO
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM) 
import enum

class event(enum.Enum):
   """
   event: Enumeration for GPIO input detection.
   """
   RISING_EDGE = 0
   FALLING_EDGE = 1
   BOTH_EDGES = 2

class output:
   """
   output: User friendly implementation for digital outputs such as leds.

           Parameters:
           __pin: Storing pin number for setting output values.
           __enabled: Indicates if the output is high (enabled) or not.
   """

   def __init__(self, pin, start_val = 0):
      """
      __init__: Initializing object for using specified GPIO pin as output.
      """
      self.__pin = pin
      self.__enabled = False 
      GPIO.setup(self.__pin, GPIO.OUT)
      GPIO.output(self.__pin, start_val)
      return

   def on(self):
      """
      on: Sets output value to high.
      """
      GPIO.output(self.__pin, 1)
      self.__enabled = True
      return

   def off(self):
      """
      off: Sets output value to low.
      """
      GPIO.output(self.__pin, 0) 
      self.__enabled = False
      return

   def toggle(self):
      """
      toggle: Toggling output value from high to low or vice versa.
      """
      if self.__enabled:
         self.off()
      else:
         self.on()
      return

   def blink(self, blink_speed_ms):
      """
      blink: Blinkning output once with specified blink speed.
      """
      for i in range(2):
         self.toggle()
         delay(blink_speed_ms)
      return

class input:
   """
   input: User friendly implementation for digital inputs such as buttons.
          Contains functionality for event detection on rising edge, falling edge
          and both edges with eligible callback routine and bouncetime.

          Parameters:
          __pin: Stores the input pin number for reading input values.
   """

   def __init__(self, pin):
      """
      __init__: Initializing object for using specified GPIO pin as input.
      """
      self.__pin = pin 
      GPIO.setup(self.__pin, GPIO.IN)
      return

   def read(self):
      """
      read: Returns input value from input pin as high (1) or low (0).
      """
      return GPIO.input(self.__pin)

   def enable_event(self, event_type, callback_routine, bouncetime = None):
      """
      enable_event: Enables event detection for specified event type on input pin.
                    which should be passed as an enumerator of the event enumeration.
                    If specified event occurs, the callback routine will be called.
                    Optional parameter bouncetime can be utilized to negate effects
                    of contact bounces if the pin is connected to a button.
      """
      if event_type == event.RISING_EDGE:
         GPIO.add_event_detect(self.__pin, GPIO.RISING, callback = callback_routine, bouncetime = bouncetime)
      elif event_type == event.FALLING_EDGE:
         GPIO.add_event_detect(self.__pin, GPIO.FALLING, callback = callback_routine, bouncetime = bouncetime)
      elif event_type == event.BOTH_EDGES:
         GPIO.add_event_detect(self.__pin, GPIO.BOTH, callback = callback_routine, bouncetime = bouncetime)
      else:
         print("Could not enable event for type " + str(event_type) + "!\n")
      return

   def disable_event(self):
      """
      disable_event: Remove event detection on input pin.
      """
      GPIO.remove_event_detect(self.__pin)
      return

def delay(delay_time_ms):
   """
   delay: Generating delay measured in milliseconds.
   """
   import time 
   time.sleep(delay_time_ms / 1000.0)
   return
