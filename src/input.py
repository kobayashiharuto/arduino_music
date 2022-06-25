from asyncore import read
from math import floor
import struct
import serial
import cv2
from cv2 import Mat
import numpy as np

NOTE_C5  = 523
NOTE_D5  = 587
NOTE_E5  = 659
NOTE_F5  = 698
NOTE_G5  = 784
NOTE_A5  = 880
NOTE_B5  = 988
NOTE_C6 = 1047
NOTE_D6 = 1175
NOTE_E6 = 1319

notes = [
    NOTE_C5,
    NOTE_D5,
    NOTE_E5,
    NOTE_F5,
    NOTE_G5,
    NOTE_A5,
    NOTE_B5,
    NOTE_C6,
    NOTE_D6,
    NOTE_E6,
]

def convert_note(position: float):
    return int(notes[floor(len(notes) * position)] / 8)


def frameEdit(frame: Mat):
    frame_width = int(frame.shape[1]/4)
    frame_height = int(frame.shape[0]/4)
    frame = cv2.resize(frame, (frame_width, frame_height))
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_lower = (30, 64, 0)
    color_higher = (90, 255, 255)

    img_th = cv2.inRange(hsv_frame, color_lower, color_higher)
    img_th = cv2.bitwise_not(img_th)

    kernel = np.ones((3,3), np.uint8)
    mask = cv2.dilate(img_th, kernel, iterations = 1)

    result = np.copy(frame)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    position = 0
    for c in contours:
        if cv2.contourArea(c) < 100: continue
        x, y, w, h = cv2.boundingRect(c)
        if w == frame_width: continue
        cv2.rectangle(result, (x, y), (x + w, y + h), (255, 255, 0), 2)
        position = (x + w / 2) / frame_width
        break
    return result, position

def main():
    cap = cv2.VideoCapture(0)

    with serial.Serial('/dev/cu.usbmodem101', 9600, timeout=1) as ser:
        while True:
            ret, frame = cap.read()

            (frame, position) = frameEdit(frame)
            cv2.imshow('Frame', frame)

            k = cv2.waitKey(1)
            if k == 27:
                break

            if position == 0:
                ser.write(struct.pack('>B', 0))   
                continue
            
            note = convert_note((1-position))
            print(position)
            ser.write(struct.pack('>B', note))

        ser.close()
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()