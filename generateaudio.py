from flask import Flask, request
import pyttsx3  # pip install pyttsx3

engine = pyttsx3.init()


def speak_finish_time(car, driver, time, split, sixtyfour=None):
    """Function to speak the finish time of the driver."""
    message = (
        "Car number "
        + car
        + " driven by "
        + driver
        + " finished in "
        + time
        + " seconds"
    )
    if split:
        message = message + " with a split of " + split + " seconds"
    if sixtyfour:
        message = message + " and a sixty four foot time of " + sixtyfour + " seconds"

    print(message)
    engine.say(message)
    engine.runAndWait()
    engine.startLoop(False)
    # engine.iterate() must be called inside Server_Up.start()
    # Server_Up = threading.Thread(target=Comm_Connection)
    # Server_Up.start()
    engine.endLoop()


def speak_class_results(thisclass):
    """Function to speak the results of a class."""
    print("Results for class " + thisclass)


app = Flask(__name__)


@app.route("/finish")
def car_finished():
    car = request.args.get("car", default=0, type=str)
    driver = request.args.get("driver", default=0, type=str)
    finish = request.args.get("finish", default=0, type=str)
    split = request.args.get("split", default=0, type=str)
    sixtyfour = request.args.get("sixtyfour", default=0, type=str)
    speak_finish_time(car, "Archie Laurence", "91.34", "46.63")
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
