#!/usr/bin/python3

################################################################################
# main.py: Implementation of GPIO with edge detection in Python.
################################################################################
import gpio 

# Global variables:
leds_enabled = False # Indicates led state (off or blinking).

def button_is_pressed(button):
   """
   button_is_pressed: Callback routine for toggling the state of the leds when
                      the button at pin 27 is pressed.
   """
   global leds_enabled
   leds_enabled = not leds_enabled
   return

def leds_blink(leds, blink_speed_ms):
   """
   leds_blink: Blinking leds stored in a list in a sequence with specified blink speed.
               Before the sequence begins, all leds are turned off.
   """
   leds_off(leds)
   for i in leds:
      i.on()
      gpio.delay(blink_speed_ms) 
      i.off()
   return

def leds_off(leds):
   """
   leds_off: Turns off leds stored in a list by setting low output signals.
   """
   for i in leds:
      i.off()
   return

def main():
   """
   main: Connecting leds to pin 17, 22 and 23 and a button to pin 27. 
         The leds are stored in a list for ease of use and ease of adding more leds.
         The leds are either blinking every 100 ms or turned off, depending on state.
         Event detection is enabled for rising edge at pin 27. When the button is 
         pressed, callback routine button_is_pressed is called to toggle the state of
         the leds between blinking (enabled) and turned off.
   """

   leds = [ gpio.output(17), gpio.output(22), gpio.output(23) ]
   button1 = gpio.input(27) 
   button1.enable_event(gpio.event.RISING_EDGE, button_is_pressed)

   while True:
      if leds_enabled:
         leds_blink(leds, 100) 
      else:
         leds_off(leds)
   return

# Calling function main to start the program if this is the startup file:
if __name__ == "__main__":
   main()