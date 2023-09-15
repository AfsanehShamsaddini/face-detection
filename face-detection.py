from cv2 import data
from PyQt5.QtGui import QPixmap
from  PyQt5.QtWidgets import  QMainWindow, QApplication,QLabel,QPushButton
from PyQt5 import uic
import sys
import cv2
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class UI(QMainWindow):
    def __init__(self,face_cascade,eye_cascade,smile_cascade):
        super(UI,self).__init__()
        uic.loadUi('face.ui',self)
        self.label = self.findChild(QLabel,"label")
        self.image_label = self.findChild(QLabel,"image1")
        self.faceimage_label = self.findChild(QLabel, "detectface")
        self.camera_btn = self.findChild(QPushButton, "camera")
        self.image_btn = self.findChild(QPushButton, "image")
        self.face_cascade= face_cascade
        self.eye_cascade = eye_cascade
        self.smile_cascade = smile_cascade
        self.show()

        self.image_btn.clicked.connect(self.image_detect)
        self.camera_btn.clicked.connect(self.camera_detect)


    def image_detect(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            '', "Image files (*.jpg *.gif)")
        self.pixmap_size = QSize(self.image_label.width(),self.image_label.height())
        self.pixmap = QPixmap(fname[0])
        self.pixmap=self.pixmap.scaled(self.pixmap_size)
        self.image_label.setPixmap(self.pixmap)
        imagepath = fname[0]
        print(imagepath)
        img = cv2.imread(imagepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # canvas = self.detect(gray, img)
        print('1')
        faces = self.face_cascade.detectMultiScale(gray, 1.301, 5)
        print("Found {0} faces".format(len(faces)))
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (100, 200, 250), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (200, 150, 250), 2)
            smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.5, 15)

            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)
        cv2.imwrite( 'face1.jpg', img)
        self.pixmap_detect_size = QSize(self.faceimage_label.width(), self.faceimage_label.height())
        print(self.pixmap_detect_size)
        self.pixmap_detect = QPixmap('face1.jpg')
        print(self.pixmap_detect)
        self.pixmap_detect = self.pixmap_detect.scaled(self.pixmap_detect_size)
        self.faceimage_label.setPixmap(self.pixmap_detect)
        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def camera_detect(self):
        video_capture = cv2.VideoCapture(0)
        while video_capture.isOpened():
            # Captures video_capture frame by frame
            _, frame = video_capture.read()
            # To capture image in monochrome
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # calls the detect() function
            faces =  self.face_cascade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
                cv2.putText(frame, "Face", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.5, 15)

                for (sx, sy, sw, sh) in smiles:
                    cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)
                    cv2.putText(roi_color, "smile", (sx, sy),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                eyes =  self.eye_cascade.detectMultiScale(roi_gray, 1.5, 10)

                # draw a rectangle around eyes
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 2)
                    cv2.putText(roi_color, "eye", (ex, ey),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)

            # Displays the result on camera feed
            cv2.imshow('img', frame)

            # Wait for Esc key to stop
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        # Release the capture once all the processing is done.
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    app=QApplication(sys.argv)
    UIWindow = UI(face_cascade,eye_cascade,smile_cascade)
    app.exec_()

