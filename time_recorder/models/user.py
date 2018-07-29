import datetime
import cv2
import numpy as np


class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.in_time = ""
        self.out_time = ""
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    def is_punch_in(self):
        if self.in_time != "":
            return True
        return False

    def punch_in(self):
        self.in_time = datetime.datetime.today()

    def punch_out(self):
        self.out_time = datetime.datetime.today()

    def working_time_sec(self):
        self.in_time = ""
        self.out_time = ""
        return (self.out_time - self.in_time).total_seconds()

    def learn(self, images, labels):
        self.recognizer.train(images, np.array(labels))

    def identification(self, face):
        label, confidence = self.recognizer.predict(face)
        print("Predicted Label: {}, Confidence: {}".format(label, confidence))

        if confidence > 90:
            print "It is my face."
        else:
            print "It is not my face"
