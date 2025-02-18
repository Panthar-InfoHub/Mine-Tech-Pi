from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)

# Define LED Pins
LED_PINS = {
    "red": 17,
    "green": 27,
    "yellow": 22
}

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setwarnings(False)

# Set all LED pins as OUTPUT
for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Ensure LEDs start OFF


@app.route('/')
def hello_world():
    return "Hello, Raspberry Pi LED Control!"


@app.route("/led/<color>/turn-on", methods=["GET"])
def turn_on_led(color):
    if color not in LED_PINS:
        return f"Invalid color: {color}. Use 'red', 'green', or 'yellow'.", 400
    
    GPIO.output(LED_PINS[color], GPIO.HIGH)
    return f"{color} LED turned ON."


@app.route("/led/<color>/turn-off", methods=["GET"])
def turn_off_led(color):
    if color not in LED_PINS:
        return f"Invalid color: {color}. Use 'red', 'green', or 'yellow'.", 400

    GPIO.output(LED_PINS[color], GPIO.LOW)
    return f"{color} LED turned OFF."


# Cleanup GPIO when stopping
@app.route("/shutdown", methods=["GET"])
def shutdown():
    GPIO.cleanup()
    return "GPIO Cleaned up and Flask server stopped."


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
