import json
from termcolor import colored
import inspect

class Log:
    @staticmethod
    def log(message="Log:", data=None, color="grey", formatjson=False):
        """Log information with a specified color"""
        if data is not None:
            if formatjson:
                try:
                    data = json.dumps(data, indent=4)
                except (TypeError, ValueError):
                    pass
            message += " " + str(data)
        if color == "red":
            frame = inspect.currentframe().f_back
            line_number = frame.f_lineno
            file_name = frame.f_globals["__file__"]
            message += f" (Issue at {file_name}, Line: {line_number})"
        if color == "grey":
            color = "white"
            attrs = ["dark"]
        else:
            attrs = []
        print(colored(message, color, attrs=attrs))

    @staticmethod
    def error(message="Log:", data=None, formatjson=False):
        message = "Error: " + message
        Log.log(message, data, "red", formatjson)

    @staticmethod
    def warning(message="Log:", data=None, formatjson=False):
        message = "Warning: " + message
        Log.log(message, data, "yellow", formatjson)

    @staticmethod
    def success(message="Log:", data=None, formatjson=False):
        Log.log(message, data, "green", formatjson)

    @staticmethod
    def info(message="Log:", data=None, formatjson=False):
        Log.log(message, data, "light_blue", formatjson)