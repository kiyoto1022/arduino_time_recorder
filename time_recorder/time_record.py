# encoding utf-8
import os
import time
import serial
from PIL import Image
from models.users import *
from models.message import *

WAIT_FOR_ACTIVATION = 3
WAIT_FOR_SAVING_COMPLETION = 1

cap = cv2.VideoCapture(0)
cascadePath = "./time_recorder/haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

users = Users()


def get_face_list_and_label(path):
    face_list = []
    labels = []
    for image in os.listdir(path):
        face = detect_face(os.path.join(path, image))
        face_list.append(face)
        labels.append(int(os.path.splitext(image)[0]))

    return face_list, labels


def detect_face(path):
    face_image = np.array(Image.open(path).convert('L'), 'uint8')

    # Detect only one face
    for (x, y, w, h) in faceCascade.detectMultiScale(face_image):
        return cv2.resize(face_image[y: y + h, x: x + w], (200, 200), interpolation=cv2.INTER_LINEAR)

    # Face undetected
    print "Face undetected"
    return ""


def shot():
    # FIXME: Is it necessary to repeat twice?
    ret, frame = cap.read()
    cv2.imwrite("./punch_out_user.jpg", frame)
    time.sleep(WAIT_FOR_SAVING_COMPLETION)
    return "./punch_out_user.jpg"


def punch_out(user):
    if not user.is_punch_in():
        print "{} is not punch in.".format(user.id)
        return

    face = detect_face(shot())
    if face == "":
        print "Face could not be detected."
        return

    # log only
    user.identification(face)

    user.punch_out
    print "{} is punch out : {}.".format(user.name, user.in_time)
    print "working time {} second.".format(user.working_time_sec())


def punch_in(user):
    if user.is_punch_in:
        print "{} is already punch in.".format(user.id)
        return

    user.punch_in
    print "{} is punch in : {}.".format(user.id, user.in_time)


def training():
    for user in users.list():
        images, labels = get_face_list_and_label("./time_recorder/data/users_face/{}".format(user.name))
        user.learn(images, labels)


def standby_camera():
    time.sleep(WAIT_FOR_ACTIVATION)
    ret, frame = cap.read()
    cv2.imwrite("test_shot.jpg", frame)


def receiving(ser):
    message = Message(ser.readline())
    if not message.is_receive():
        return

    if not users.is_member(message.user_id):
        print "{} is not member.".format(message.user_id)
        return

    if message.is_punch_in():
        punch_in(users.get(message.user_id))

    if message.is_punch_out():
        punch_out(users.get(message.user_id))


def main():
    ser = serial.Serial('COM3', 9600, timeout=1)
    while True:
        receiving(ser)


if __name__ == "__main__":
    training()
    standby_camera()
    main()
