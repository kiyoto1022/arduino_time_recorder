# encoding utf-8
import os
import time
import serial
import cv2
from PIL import Image
import numpy as np
from models.users import Users
from models.message import Message

WAIT_FOR_ACTIVATION = 3
WAIT_FOR_SAVING_COMPLETION = 1

cap = cv2.VideoCapture(0)
cascadePath = "./haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

users = Users()


def training():
    for user in users.list():
        images, labels = get_face_list_and_label("./data/users_face/{}".format(user.name))
        user.learn(images, labels)


def standby_camera():
    time.sleep(WAIT_FOR_ACTIVATION)
    ret, frame = cap.read()
    cv2.imwrite("test_shot.jpg", frame)


def detect_face(path):
    face_image = np.array(Image.open(path).convert('L'), 'uint8')

    # Detect only one face
    for (x, y, w, h) in faceCascade.detectMultiScale(face_image):
        return cv2.resize(face_image[y: y + h, x: x + w], (200, 200), interpolation=cv2.INTER_LINEAR)

    print "Face undetected"
    return None


def get_face_list_and_label(path):
    face_list = []
    labels = []
    for image in os.listdir(path):
        face = detect_face(os.path.join(path, image))
        if face is not None:
            face_list.append(face)
            labels.append(int(os.path.splitext(image)[0]))

    return face_list, labels


def shot():
    while True:
        ret, frame = cap.read()
        cv2.imwrite("./punch_out_user.jpg", frame)
        time.sleep(WAIT_FOR_SAVING_COMPLETION)

        face = detect_face("./punch_out_user.jpg")
        if face is None:
            print "Face could not be detected"
            continue
        return face


def receiving(ser):
    message = Message(ser.readline())
    if not message.is_receive():
        return

    if not users.is_member(message.user_id):
        print "{} is not member".format(message.user_id)
        return

    user = users.get(message.user_id)
    if message.is_punch_in():
        user.punch_in()

    if message.is_punch_out():
        if not user.is_punch_in():
            print "{} is not punch in".format(user.id)
            return
        user.punch_out(shot())


def main():
    ser = serial.Serial('COM3', 9600, timeout=1)
    while True:
        receiving(ser)


if __name__ == "__main__":
    training()
    standby_camera()
    main()
