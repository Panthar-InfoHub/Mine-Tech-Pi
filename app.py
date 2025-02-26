from flask import Flask
from gpiozero import LED

app = Flask(__name__)

# Define LED Pins using gpiozero
LED_PINS = {
    "red": LED(17),
    "green": LED(27),
    "yellow": LED(22)
}


@app.route('/')
def hello_world():
    return "Hello, Raspberry Pi LED Control with gpiozero!"


@app.route("/led/<color>/turn-on", methods=["GET"])
def turn_on_led(color):
    if color not in LED_PINS:
        return f"Invalid color: {color}. Use 'red', 'green', or 'yellow'.", 400

    LED_PINS[color].on()
    return f"{color} LED turned ON."


@app.route("/led/<color>/turn-off", methods=["GET"])
def turn_off_led(color):
    if color not in LED_PINS:
        return f"Invalid color: {color}. Use 'red', 'green', or 'yellow'.", 400

    LED_PINS[color].off()
    return f"{color} LED turned OFF."


# Cleanup GPIO when stopping
@app.route("/shutdown", methods=["GET"])
def shutdown():
    for led in LED_PINS.values():
        led.close()  # Clean up LED resources
    return "GPIO Cleaned up and Flask server stopped."


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)