import os
from ultralytics import YOLO
import supervision as sv
import cv2
import serial
from tkinter import filedialog
import tkinter as tk
import win32event
import win32api
import sys
from winerror import ERROR_ALREADY_EXISTS
mutex = win32event.CreateMutex(None, False, 'name')
last_error = win32api.GetLastError()
if last_error == ERROR_ALREADY_EXISTS:
    sys.exit(0)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


root = tk.Tk()
root.title("Simple Coin Detection App")
width = 400  # Width
height = 500  # Height

arduinoData = serial.Serial('COM3', 115200)


def select_image():
    sum = 0.00
    count = 0
    file_path = filedialog.askopenfilename(title="Select an image",
                                           filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])

    frame = cv2.imread(file_path)
    model = YOLO(resource_path('coinfinal.pt'))
    result = model.predict(frame, conf=.64)[0]
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
    detections = sv.Detections.from_yolov8(result)
    labels = [
        f"{model.model.names[class_id]} {confidence:0.2f}"
        for _, confidence, class_id, _
        in detections
    ]
    label = [
        f"{model.model.names[class_id]}"
        for _, confidence, class_id, _
        in detections
    ]
    frame = box_annotator.annotate(
        scene=frame,
        detections=detections,
        labels=labels
    )
    resize = cv2.resize(frame, (640, 512))
    cv2.imshow('Result', resize)
    cv2.imwrite('Result', resize)
    # formatted_sum = f"{sum:.2f}"
    # print(len(label))
    # print(sum)
    arduinoData.write(f"{len(label)}, {sum:.2f}\r".encode())
    cv2.waitKey(0)
    cv2.destroyAllWindows


def capture_video():
    # Open the default camera (usually camera index 0)
    cap = cv2.VideoCapture(1)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        sum = 0
        count = 0
        cv2.imshow("Camera", frame)
        key = cv2.waitKey(5)
        if key % 256 == 27:
            break
        elif key % 256 == 32:
            img = "Image.jpg".format()
            cv2.imwrite(img, frame)
            input = cv2.imread(img)
            model = YOLO(resource_path('coinfinal.pt'))
            result = model.predict(input, conf=0.64)[0]
            box_annotator = sv.BoxAnnotator(
                thickness=2,
                text_thickness=2,
                text_scale=1
            )
            detections = sv.Detections.from_yolov8(result)
            labels = [
                f"{model.model.names[class_id]} {confidence:0.2f}"
                for _, confidence, class_id, _
                in detections
            ]
            label = [
                f"{model.model.names[class_id]}"
                for _, confidence, class_id, _
                in detections
            ]
            input = box_annotator.annotate(
                scene=input,
                detections=detections,
                labels=labels
            )
            for target in label:
                if target == '5-cent':
                    sum += 0.05
                if target == '25-cent':
                    sum += 0.25
                if target == 'Coins-F6FW':
                    sum += 1
                if target == '5 peso':
                    sum += 5
                if target == '10 Peso':
                    sum += 10
                if target == '20 Peso':
                    sum += 20
                count += 1
            resize = cv2.resize(input, (640, 512))
            # formatted_sum = f"{sum:.2f}"
            # print(count)
            # print(sum)
            cv2.imshow('frame', resize)
            arduinoData.write(f"{count}, {sum:.2f}\r".encode())
    cap.release
    cv2.destroyAllWindows()


screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight()  # Height of the screen

# Calculate Starting X and Y coordinates for Window
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)

root.geometry('%dx%d+%d+%d' % (width, height, x, y))

frame = tk.Frame(root, width=500, height=600, bg="#3d6466")
frame.grid(row=0, column=0)
frame.pack_propagate(False)
frame.pack(expand=True)

tk.Button(frame, text="Use Camera", font=("TkHeadingFont", 20), bg="#28393a", fg="white",
          cursor="hand2", activebackground="#badee2", activeforeground="black", command=lambda: capture_video()).pack(side="top", pady=100)

tk.Button(frame, text="Upload Image", font=("TkHeadingFont", 20), bg="#28393a", fg="white",
          cursor="hand2", activebackground="#badee2", activeforeground="black", command=lambda: select_image()).pack(side="top", pady=10)

root.mainloop()
