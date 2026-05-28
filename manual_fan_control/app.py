from flask import Flask, render_template, request, jsonify
import os
import time
import socket
from zeroconf import ServiceInfo, Zeroconf

app = Flask(__name__)

# This is a placeholder for your relay control logic
# In a real scenario, you would interact with GPIO pins (e.g., on a Raspberry Pi)
# For example:
# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)
# RELAY_PIN = 17 # Example GPIO pin
# GPIO.setup(RELAY_PIN, GPIO.OUT)

fan_state = "off" # Initial state

@app.route('/')
def index():
    return render_template('index.html', fan_state=fan_state)

@app.route('/toggle_fan', methods=['POST'])
def toggle_fan():
    global fan_state
    if fan_state == "off":
        fan_state = "on"
        # In a real scenario, activate the relay
        # GPIO.output(RELAY_PIN, GPIO.HIGH)
        print("Fan turned ON")
    else:
        fan_state = "off"
        # In a real scenario, deactivate the relay
        # GPIO.output(RELAY_PIN, GPIO.LOW)
        print("Fan turned OFF")
    return jsonify(status="success", new_state=fan_state)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('manual_fan_control/templates', exist_ok=True)

    # Zeroconf (mDNS) setup
    zeroconf_instance = None
    service_info = None
    server_port = 5000
    try:
        # Get host IP address dynamically
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) # Connect to a public server to get local IP
        host_ip = s.getsockname()[0]
        s.close()
        
        info = ServiceInfo(
            "_http._tcp.local.",
            "Fan Control Webserver._http._tcp.local.",
            addresses=[socket.inet_aton(host_ip)],
            port=server_port,
            properties={'path': '/'},
            server="fancontrol.local.",
        )
        print(f"Registering service: {info}")
        zeroconf_instance = Zeroconf()
        zeroconf_instance.register_service(info)
        print("Zeroconf service registered.")
        
        app.run(host='0.0.0.0', port=server_port, debug=True, use_reloader=False) # use_reloader=False to prevent multiple zeroconf registrations
    finally:
        if zeroconf_instance and info:
            print("Unregistering Zeroconf service...")
            zeroconf_instance.unregister_service(info)
            zeroconf_instance.close()
            print("Zeroconf service unregistered and closed.")
