import socket
import RPi.GPIO as GPIO

LED_PIN = 2  # เปลี่ยนเป็นขา GPIO ที่ต้องการ
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def web_page():
    html = """<!DOCTYPE html>
<html>
<head><title>Raspberry Pi Web Server</title></head>
<body><h1>Hello from Raspberry Pi!</h1>
<p>Use ?action=yes to turn ON LED, ?action=no to turn OFF LED.</p>
</body>
</html>"""
    return html

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 8080))  # ใช้ port 8080 (หรือ 80 ถ้าไม่ติดสิทธิ์)
    s.listen(5)
    print("Web server listening on port 8080")

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024).decode()
        print('Content = %s' % request)

        # Check for action in GET request
        if '/?action=yes' in request:
            GPIO.output(LED_PIN, GPIO.HIGH)
            print('LED ON')
        elif '/?action=no' in request:
            GPIO.output(LED_PIN, GPIO.LOW)
            print('LED OFF')

        response = web_page()
        conn.send(b'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response.encode())
        conn.close()

if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        GPIO.cleanup()