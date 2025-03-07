
import os
import logging
from flask import Flask, jsonify, request
# from gpiozero import LED
from ai import analyze_video
import json
# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('suraksha.api')

# Define LED Pins
# LED_PINS = {
#     "red": LED(17),
#     "green": LED(27),
#     "yellow": LED(22)
# }


@app.route("/")
def home():
    return jsonify({"message": "Hello, Raspberry Pi LED Control API is running!"})


# def turn_on_led(color):
#     if color not in LED_PINS:
#         print(f"Invalid color: {color}. Use 'red', 'green', or 'yellow'.")
#         return
#
#     LED_PINS[color].on()
#     logging.info(f"{color} LED turned ON")
#     return
# def turn_off_led(color):
#     if color not in LED_PINS:
#         logging.error(f"Invalid color: {color}. Use 'red', 'green', or 'yellow'.")
#         return
#
#     LED_PINS[color].off()
#     logging.info(f"{color} LED turned OFF")
#     return
# def turn_off_all():
#     for led in LED_PINS.values():
#         led.off()
#     logging.info("All LEDs turned OFF")


# @app.route("/shutdown", methods=["GET"])
# def shutdown():
#     for led in LED_PINS.values():
#         led.close()  # Clean up LED resources
#     logging.info("GPIO Cleaned up and Flask server stopped")
#     return jsonify({"message": "GPIO Cleaned up and Flask server stopped"}), 200


@app.route("/media/process/video", methods=["POST"])
def process_video():
    try:
        data = request.get_json()
        logging.debug(f"Request payload: {json.dumps(data, indent=2)}")

        # Check if 'bucket_urls' is present and is a non-empty array of strings
        if not data or 'bucket_urls' not in data or not isinstance(data['bucket_urls'], list) or not all(
                isinstance(url, str) for url in data['bucket_urls']) or not data['bucket_urls']:
            logger.error("Invalid or empty 'bucket_urls' in request payload")
            return jsonify({'error': "Invalid or empty 'bucket_urls'"}), 400

        # Call the placeholder function and return its response
        logger.info("Calling Generation function")
        response = analyze_video(bucket_urls=data["bucket_urls"])

        # Add condition to ensure only heavy vehicles carrying mining or heavy goods are processed
        if not isinstance(response, list) or not response:
            logger.error("Invalid response format from analyze_video")
            return jsonify({'error': "Invalid response from video analysis", "res": response}), 500

        vehicle_data = response[0]  # Assuming the response list contains the analyzed data for a single vehicle
        if (
                vehicle_data.get("vehicle_type") not in ["Truck", "Heavy Load"] or
                not vehicle_data.get("is_carrying_contents") or
                vehicle_data.get("contents_details") not in ["mining", "heavy goods"]
        ):
            logger.warning("Vehicle does not meet the criteria for heavy vehicle and mining/heavy goods")
            return jsonify({'error': "Vehicle does not meet the criteria"}), 400

        return response, 200

    except Exception as exception:
        logger.error(f"Error processing image: {str(exception)}", exc_info=True)
        return jsonify({'error': 'Internal Server Error', 'message': str(exception)}), 500




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)