from machine import Pin
import time

# Define the GPIO pin connected to the LED
# The onboard LED on many ESP32 boards is connected to GPIO2
led_pin = Pin(2, Pin.OUT)

while True:
    led_pin.value(1)  # Turn LED on (high)
    print("ON")
    time.sleep(1)     # Wait for 1 second
    led_pin.value(0)  # Turn LED off (low)
    time.sleep(1)     # Wait for 1 second
display.show('12')
