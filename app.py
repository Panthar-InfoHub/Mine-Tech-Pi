from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route("/led/<color>/turn-on", methods=["GET"])
def turn_on_led(color):
    if color not in ["red", "green", "yellow"]:  # Check if the color is valid
        return f"Invalid color: {color}. Please use 'red', 'green', or 'yellow'.", 400

    print(f"Turning on {color} LED.")
    return f"{color} LED turned on."


@app.route("/led/<color>/turn-off", methods=["GET"])
def turn_off_led(color):
    if color not in ["red", "green", "yellow"]:  # Check if the color is valid
        return f"Invalid color: {color}. Please use 'red', 'green', or 'yellow'.", 400


    print(f"Turning off {color} LED.")
    return f"{color} LED turned off."


if __name__ == '__main__':
    app.run(port=8080)
