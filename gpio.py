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
   RISING_EDGE = 0  # Input value from low to high.
   FALLING_EDGE = 1 # Input value from high to low. 
   BOTH_EDGES = 2   # Change in input value.

class output:
   """
   output: User friendly implementation for digital outputs such as leds.

           Parameters:
           __pin: Storing pin number for setting output values.
           __enabled: Indicates if the output is high (enabled) or not.
   """

   def __init__(self, pin, start_val = 0):
      """
      __init__: Initializing specified GPIO pin as output.

                - self: Reference to the GPIO output.
                - pin : The GPIO output pin number.
                - start_val: Output start value, (0 = low, 1 = high).
                             Default value is set to 0 for low output starting value.
      """
      self.__pin = pin
      self.__enabled = False 
      GPIO.setup(self.__pin, GPIO.OUT)
      GPIO.output(self.__pin, start_val)
      return

   def __del__(self):
      """
      __del__: Setting low output value on pin and resetting data direction
               to input when the object is deleted.

               - self: Reference to the GPIO output.
      """
      GPIO.output(self.__pin, 0)
      GPIO.setup(self.__pin, GPIO.IN)
      return

   def pin(self):
      """
      pin: Returning GPIO output pin number.

           - self: Reference to the GPIO output.
      """
      return self.__pin

   def enabled(self):
      """
      enabled: Indicates whether GPIO output value by returning boolean value,
               where True = high, False = low.

               - self: Reference to the GPIO output.
      """
      return self.__enabled

   def on(self):
      """
      on: Sets GPIO output value to high.
      
          - self: Reference to the GPIO output.
      """
      GPIO.output(self.__pin, 1)
      self.__enabled = True
      return

   def off(self):
      """
      off: Sets GPIO output value to low.

           - self: Reference to the GPIO output.
      """
      GPIO.output(self.__pin, 0) 
      self.__enabled = False
      return

   def toggle(self):
      """
      toggle: Toggling GPIO output value from high to low or vice versa.

              - self: Reference to the GPIO output.
      """
      if self.__enabled:
         self.off()
      else:
         self.on()
      return

   def blink(self, blink_speed_ms):
      """
      blink: Blinkning GPIO output once with specified blink speed.

             - self          : Reference to the GPIO output.
             - blink_speed_ms: Blink speed in milliseconds.
      """
      for i in range(2):
         self.toggle()
         delay(blink_speed_ms)
      return

class input:
   """
   input: User friendly implementation for digital inputs such as buttons.
          No destructor is needed in this example.

          Parameters:
          __pin: Stores the input pin number for reading input values.
   """

   def __init__(self, pin):
      """
      __init__: Initializing specified GPIO pin as input.

                - self: Reference to the GPIO input.
                - pin : The GPIO input pin number.
      """
      self.__pin = pin 
      GPIO.setup(self.__pin, GPIO.IN)
      return

   def __del__(self):
      """
      __del__: Disabling potential event detection when GPIO input object is deleted.

               - self: Reference to the GPIO input.
      """
      GPIO.remove_event_detect(self.__pin) 
      return

   def read(self):
      """
      read: Returns input value from input pin as True (high) or False (low).

            - self: Reference to the GPIO input.
      """
      return GPIO.input(self.__pin)

   def enable_event(self, event_type, callback_routine, bouncetime = None):
      """
      enable_event: Enables event detection for specified event type on input pin.
                    which should be passed as an enumerator of the event enumeration.
                    If specified event occurs, the callback routine will be called.
                    Optional parameter bouncetime can be utilized to negate effects
                    of contact bounces if the pin is connected to a button.

                    - self            : Reference to the GPIO input.
                    - event_type      : Specifies flank for event detection (rising, falling, both).
                    - callback_routine: The routine to be called when specified event is detected.
                    - bouncetime      : Time in milliseconds to be elapsed before event detection,
                                        which is beneficial for reducing effects of contact bounces.

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

                     - self: Reference to the GPIO input.
      """
      GPIO.remove_event_detect(self.__pin)
      return

def delay(delay_time_ms):
   """
   delay: Generating delay measured in milliseconds.

          - delay_time_ms: Required delay time in milliseconds.
   """
   import time 
   time.sleep(delay_time_ms / 1000.0)
   return
