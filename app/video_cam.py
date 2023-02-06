import asyncio

import cv2
import threading


def gen(camera_obj):
    while True:
        frame_bytes, frame = camera_obj.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


class VideoCamera(object):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(r"C:\Users\Lpantskhava\Documents\R&D Projects\ajaxproj\ajaxdemo\app\static\app\haarcascade_profileface.xml")
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        (self.grabbed, self.frame) = self.video.read()
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        try:
            x, y, w, h = faces[0]
            self.frame = cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        except:
            pass
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes(), jpeg

    def update(self):
        while True:
            if self.video.isOpened():
                (self.grabbed, self.frame) = self.video.read()
                black_white = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(black_white, 1.1, 4)
                try:
                    x, y, w, h = faces[0]
                    self.frame = cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                except:
                    pass