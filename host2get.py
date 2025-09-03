import network
import socket
import time
 
from machine import Pin


SSID = 'Amscool'
PASSWORD = 'Am88888888'

led_pin = Pin(2, Pin.OUT)

def blink():
    global led_pin
    while True:
        led_pin.value(1)  # Turn LED on (high)
        time.sleep(1)     # Wait for 1 second
        led_pin.value(0)  # Turn LED off (low)
        time.sleep(1)     # Wait for 1 second

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print('Network config:', wlan.ifconfig())
    return wlan.ifconfig()[0]

def web_page():
    html = """<!DOCTYPE html>
<html>
<head><title>ESP32 Web Server</title></head>
<body><h1>Hello from ESP32!</h1>
<p>Use ?action=yes to turn ON LED, ?action=no to turn OFF LED.</p>
</body>
</html>"""
    return html

def start_server():
    ip_address = connect_wifi()
    if not ip_address:
        print("Failed to connect to Wi-Fi. Exiting.")
        return

    print("Web server listening on http://%s/" % ip_address)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request_str = str(request)
        print('Content = %s' % request_str)

        # Check for action in GET request
        if '/?action=yes' in request_str:
            led_pin.value(0)
            #blink()
            print('LED ON')
           
        elif '/?action=no' in request_str:
            led_pin.value(1)
            print('LED OFF')
          

        response = web_page()
        conn.send(b'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response.encode())
        conn.close()

start_server()
