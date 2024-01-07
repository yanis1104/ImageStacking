import cv2
import numpy as np
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QFileDialog, QLabel, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QImage, QPixmap

import Video
import Variance

#def old():
    ## Chemin vers le dossier contenant les images
    #images_folder = 'video_crop'
    #
    ## Liste pour stocker les images
    #image_list = []
    #
    ## Charger les images dans la séquence
    #for image_file in sorted(os.listdir(images_folder)):
    #    if image_file.endswith('.png'):
    #        image_path = os.path.join(images_folder, image_file)
    #        image = cv.imread(image_path)
    #        image_list.append(image)
    #
    ## Empiler les images en une seule structure de données
    #stacked_images = np.stack(image_list, axis=0)
    #
    ## Calculer la médiane des images empilées
    #median_image = np.median(stacked_images, axis=0).astype(np.uint16)
    #
    ## Afficher l'image médiane
    #median_image = (median_image.astype('float32') / 255 * 65535).astype('uint16')
    #cv.imwrite('ImageMediane.tif', median_image, [cv.IMWRITE_TIFF_COMPRESSION, 1])
    #
    #
    
##################################

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.filename = None
        self.video = None
        self.video_is_paused = True
        self.video_label = QLabel(self)
        self.frame_index = 0
        self.cursor_moved_by_user = False
        self.close_program = False

        self.frames = {}

        self.initGUI()




    def openFile(self):
        pass

    def createOpenFileButton(self, data_load_layout :QVBoxLayout):
        # Création d'un bouton
        open_file_button = QPushButton('Open file', self)
        open_file_button.setMaximumSize(100, 30)
        open_file_button.clicked.connect(self.openFile)
        # Ajoute le bouton au layout
        data_load_layout.addWidget(open_file_button)

    def playVideo(self):
        pass

    def createPlayButton(self, data_video_layout :QVBoxLayout):
        # Création d'un bouton
        self.play_video_button = QPushButton('Play', self)
        self.play_video_button.setMaximumSize(50, 30)
        self.play_video_button.setEnabled(False)
        self.play_video_button.clicked.connect(self.playVideo)
        # Ajoute le bouton au layout
        data_video_layout.addWidget(self.play_video_button)

    def analyzeVideo(self):
        self.frame_index = 0
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)
        while(True):
            ret, frame = self.video.read()
            if ret:
                variance = Variance.get_variance(frame)
                self.frames[self.frame_index] = variance
                print(self.frames[self.frame_index])
                self.frame_index += 1
            else:
                break
        self.frame_index = 0
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)

    def createAnalyzeButton(self, data_analyze_layout :QVBoxLayout):
        self.analyze_button = QPushButton('Analyze', self)
        self.analyze_button.setMaximumSize(50, 30)
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self.analyzeVideo)
        data_analyze_layout.addWidget(self.analyze_button)

    def accessFrameIndex(self):
        if self.cursor_moved_by_user:
            self.frame_index = self.trackbar.value()
            if not self.video.isOpened():
                QMessageBox.information(self, 'Error', 'Cannot open file')
                return
            self.video.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)
            self.showFrameVideo()
            self.trackbar_label.setText(str(self.trackbar.value()))

    def play(self):
        self.cursor_moved_by_user = False

    def pause(self):
        self.cursor_moved_by_user = True

    def createTrackBar(self, data_video_layout :QVBoxLayout):
        self.trackbar = QSlider(self)
        self.trackbar.setOrientation(1)
        self.trackbar.setMinimum(0)
        self.trackbar.setMaximum(0)
        self.trackbar.setValue(0)
        self.trackbar.valueChanged.connect(self.accessFrameIndex)
        self.trackbar.sliderPressed.connect(self.pause)
        self.trackbar.sliderReleased.connect(self.play)

        self.trackbar_label = QLabel("0")

        data_video_layout.addWidget(self.trackbar_label)
        data_video_layout.addWidget(self.trackbar)

    def updateIndex(self):
        if self.frame_index < self.video_len:
            self.frame_index += 1
            self.trackbar.setValue(self.frame_index)
            self.trackbar_label.setText(str(self.trackbar.value()))

    def showFrameVideo(self):
        pass

    def openVideo(self):
        pass

    def initGUI(self):
        self.setWindowTitle('Image Stacker')
        self.setGeometry(100, 100, 1500, 800)  # Définit la position et la taille de la fenêtre

        # Création d'un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)


        # Création des layout
        main_layout = QHBoxLayout()
        data_layout = QVBoxLayout()
        data_handler_layout = QHBoxLayout()
        data_load_layout = QVBoxLayout()
        data_view_layout = QVBoxLayout()
        data_video_layout = QVBoxLayout()

        data_settings_layout = QVBoxLayout()
        data_analyze_layout = QVBoxLayout()
        data_stack_layout = QVBoxLayout()
        data_log_layout = QVBoxLayout()


        # Définit le layout du widget central
        central_widget.setLayout(main_layout)

        main_layout.addLayout(data_layout)
        data_layout.addLayout(data_handler_layout)
        data_handler_layout.addLayout(data_load_layout)
        data_handler_layout.addLayout(data_view_layout)
        data_handler_layout.addLayout(data_video_layout)

        main_layout.addLayout(data_settings_layout)
        data_settings_layout.addLayout(data_analyze_layout)
        data_settings_layout.addLayout(data_stack_layout)
        data_settings_layout.addLayout(data_log_layout)

        self.createOpenFileButton(data_load_layout)
        self.createPlayButton(data_video_layout)
        self.createTrackBar(data_handler_layout)
        self.createAnalyzeButton(data_analyze_layout)

        self.video_size_factor = 1.0
        data_layout.addWidget(self.video_label)

    def closeEvent(self, event):
        # Libérer les ressources ou effectuer d'autres opérations à la fermeture
        if self.video and self.video.isOpened():
            self.video.release()
            self.video_is_paused = False
            self.close_program = True

        event.accept()

GUI.openFile = Video.openFile
GUI.openVideo = Video.openVideo
GUI.showFrameVideo = Video.showFrameVideo
GUI.playVideo = Video.playVideo

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())