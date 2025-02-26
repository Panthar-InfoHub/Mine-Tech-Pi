import os
import logging
from flask import Flask, jsonify
from gpiozero import LED

# Initialize Flask app
app = Flask(__name__)

# Configure Logging
logging.basicConfig(level=logging.INFO)

# Define LED Pins
LED_PINS = {
    "red": LED(17),
    "green": LED(27),
    "yellow": LED(22)
}


@app.route("/")
def home():
    return jsonify({"message": "Hello, Raspberry Pi LED Control API is running!"})


@app.route("/led/<color>/turn-on", methods=["GET"])
def turn_on_led(color):
    if color not in LED_PINS:
        return jsonify({"error": f"Invalid color: {color}. Use 'red', 'green', or 'yellow'."}), 400

    LED_PINS[color].on()
    logging.info(f"{color} LED turned ON")
    return jsonify({"message": f"{color} LED turned ON"}), 200


@app.route("/led/<color>/turn-off", methods=["GET"])
def turn_off_led(color):
    if color not in LED_PINS:
        return jsonify({"error": f"Invalid color: {color}. Use 'red', 'green', or 'yellow'."}), 400

    LED_PINS[color].off()
    logging.info(f"{color} LED turned OFF")
    return jsonify({"message": f"{color} LED turned OFF"}), 200


@app.route("/led/turn-on-all", methods=["GET"])
def turn_on_all():
    for led in LED_PINS.values():
        led.on()
    logging.info("All LEDs turned ON")
    return jsonify({"message": "All LEDs turned ON"}), 200


@app.route("/led/turn-off-all", methods=["GET"])
def turn_off_all():
    for led in LED_PINS.values():
        led.off()
    logging.info("All LEDs turned OFF")
    return jsonify({"message": "All LEDs turned OFF"}), 200


@app.route("/shutdown", methods=["GET"])
def shutdown():
    for led in LED_PINS.values():
        led.close()  # Clean up LED resources
    logging.info("GPIO Cleaned up and Flask server stopped")
    return jsonify({"message": "GPIO Cleaned up and Flask server stopped"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)