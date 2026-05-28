from flask import Flask, render_template, request, jsonify
import os
import time

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
    app.run(host='0.0.0.0', port=5000, debug=True)
