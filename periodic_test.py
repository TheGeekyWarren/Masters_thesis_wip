import time, threading
from pynput import mouse
from picamera2 import Picamera2, Preview
import os
from datetime import datetime as dt
import sched2 as sched

start = time.monotonic()
cap_rate = 20
slp_tm = round(1/cap_rate, 3)

def cap_img():
    on = time.monotonic()
    global trial_n
    file_path = "trial_"+str(trial_n)+".jpg"
    tr_on = time.monotonic()
    picam2.capture_file(file_path)
    tr_off = time.monotonic()
    trial_n = trial_n+1
    print("Length of img capture - ", (tr_off-tr_on)*1000)
    print("exec time = ", (time.monotonic()-on)*1000)

def on_click(x, y, button, pressed):
    global stop, session
    if pressed:
        if button==button.right:
            print("Starting recording")
            stop = False
        if button==button.left:
            print("Stopping recording") 
            stop = True
        if button==button.middle:
            print("Exiting")
            session = False
            return False

def runs():
    global slp_tm, start, stop, session
    print()
    print()
    if not session:
        metadata = picam2.capture_metadata()
        print(metadata)
        picam2.stop_preview()
    if session:
        bef = time.monotonic()
        print("Before - ", (bef-start)*1000)
        if stop:
            print(stop)
            cap_img()
        else:
            print(stop)
        aft = time.monotonic()
        print("After = ", (aft-start)*1000)
        print("time diff = ", aft-bef)
        start = time.monotonic()
        threading.Timer(slp_tm, runs).start()
        
picam2 = Picamera2()
"""exp_tm = 3000
anlg_gn = exp_tm/1000"""
camera_config = picam2.create_still_configuration(controls={"ExposureTime": 2000, "AnalogueGain": 9.0}, main={"size": (1280, 720)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()

# Create a folder on the desktop with the current date if it doesn't exist
folder_path = os.path.expanduser('~/Desktop/{}'.format(dt.now().strftime('%Y-%m-%d')))
os.makedirs(folder_path, exist_ok=True)
os.chdir(folder_path)

# Create a scheduler
scheduler = sched.scheduler(time.monotonic, time.sleep)
trial_n = 1

stop = False
session = True

listener = mouse.Listener(on_click=on_click)
listener.start()

runs()
