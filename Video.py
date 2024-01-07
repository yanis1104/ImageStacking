import cv2
import numpy as np
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QFileDialog, QLabel, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QImage, QPixmap

def openVideo(self):
    if not self.video.isOpened():
        QMessageBox.information(self, 'Error', 'Cannot open file')
        return

    self.play_video_button.setEnabled(True)
    self.analyse_button.setEnabled(True)
    self.video_len = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
    self.trackbar.setMinimum(0)
    self.trackbar.setMaximum(self.video_len - 1)
    self.frame_index = 0
    self.frames = {}
    self.sorted_frames_index = []
    self.is_video_analysed = False

def openFile(self):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    self.filename, _ = QFileDialog.getOpenFileName(self, 'Ouvrir', '', 'SER Files (*.ser);;MP4 Files (*.mp4);;All Files (*)', options=options)

    if self.filename:
        self.video = cv2.VideoCapture(self.filename)
        self.openVideo()
        self.trackbar.setValue(0)
        self.showFrameVideo()

def playVideo(self):
    self.video_is_paused = not self.video_is_paused
    if not self.video_is_paused:
        self.play_video_button.setText("Pause")
        while not self.close_program:
        # Si video en pause
            while self.video_is_paused:
                QApplication.processEvents()
            if self.showFrameVideo() == 0:
                self.trackbar.setValue(0)
                self.trackbar_label.setText(str(self.trackbar.value()))
            else:
                self.updateIndex()
                
    self.play_video_button.setText("Play")

def showFrameVideo(self):
    if self.is_video_analysed:
        if self.frame_index < self.video_len:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, self.sorted_frames_index[self.frame_index])

    ret, frame = self.video.read()

    # Si la lecture de la vidéo est terminée
    if not ret:
        self.frame_index = 0
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)
        return 0

    frame = cv2.resize(frame, None, fx=self.video_size_factor, fy=self.video_size_factor)

    # Convertir l'image OpenCV en QImage
    height, width, channel = frame.shape
    bytesPerLine = 3 * width
    qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

    # Afficher l'image dans le QLabel
    pixmap = QPixmap.fromImage(qImg)
    self.video_label.setPixmap(pixmap)

    # Rafraîchir l'affichage
    QApplication.processEvents()

    if not ret:
        self.frame_index = 0
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)
        return 0
    return 1
