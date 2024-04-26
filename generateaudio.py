from flask import Flask
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


def speak_class_results(thisclass):
    """Function to speak the results of a class."""
    print("Results for class " + thisclass)


speak_finish_time("69", "Archie Laurence", "91.34", "46.63")
