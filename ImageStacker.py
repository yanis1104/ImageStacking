import cv2
import numpy as np
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QFileDialog, QLabel, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QImage, QPixmap

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

        self.initGUI()




    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Ouvrir', '', 'SER Files (*.ser);;MP4 Files (*.mp4);;All Files (*)', options=options)

        if self.filename:
            self.video = cv2.VideoCapture(self.filename)
            self.readVideo()
            self.frame_index = 1

    def createOpenFileButton(self, data_load_layout :QVBoxLayout):
        # Création d'un bouton
        open_file_button = QPushButton('Open file', self)
        open_file_button.setMaximumSize(100, 30)
        open_file_button.clicked.connect(self.openFile)
        # Ajoute le bouton au layout
        data_load_layout.addWidget(open_file_button)

    def playVideo(self):
        self.video_is_paused = not self.video_is_paused

    def createPlayButton(self, data_video_layout :QVBoxLayout):
        # Création d'un bouton
        self.play_video_button = QPushButton('Play', self)
        self.play_video_button.setMaximumSize(50, 30)
        self.play_video_button.setEnabled(False)
        self.play_video_button.clicked.connect(self.playVideo)
        # Ajoute le bouton au layout
        data_video_layout.addWidget(self.play_video_button)

    def accessFrameIndex(self):
        self.frame_index = self.trackbar.value()
        if not self.video.isOpened():
            QMessageBox.information(self, 'Error', 'Cannot open file')
            return
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index - 1)
        self.showFrameVideo()

    def createTrackBar(self, data_video_layout :QVBoxLayout):
        self.trackbar = QSlider(self)
        self.trackbar.setOrientation(1)
        self.trackbar.setMinimum(0)
        self.trackbar.setMaximum(0)
        self.trackbar.valueChanged.connect(self.accessFrameIndex)

        data_video_layout.addWidget(self.trackbar)

    def showFrameVideo(self):
        ret, frame = self.video.read()

        # Si la lecture de la vidéo est terminée
        if not ret:
            return 0

        print(self.frame_index)
        self.frame_index += 1
        self.trackbar.setValue(self.frame_index - 1)

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
            return 0
        return 1

    def readVideo(self):
        if not self.video.isOpened():
            QMessageBox.information(self, 'Error', 'Cannot open file')
            return

        self.play_video_button.setEnabled(True)
        self.video_len = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.trackbar.setMinimum(1)
        self.trackbar.setMaximum(self.video_len)
        
        while True:
            # Si video en pause
            while self.video_is_paused:
                QApplication.processEvents()
            if self.showFrameVideo() == 0:
                break
            

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


        # Définit le layout du widget central
        central_widget.setLayout(main_layout)

        main_layout.addLayout(data_layout)
        data_layout.addLayout(data_handler_layout)
        data_handler_layout.addLayout(data_load_layout)
        data_handler_layout.addLayout(data_view_layout)
        data_handler_layout.addLayout(data_video_layout)

        self.createOpenFileButton(data_load_layout)
        self.createPlayButton(data_video_layout)
        self.createTrackBar(data_handler_layout)

        self.video_size_factor = 1.0
        data_layout.addWidget(self.video_label)

    def closeEvent(self, event):
        # Libérer les ressources ou effectuer d'autres opérations à la fermeture
        if self.video and self.video.isOpened():
            self.video.release()
            self.video_is_paused = False
            self.play_video_button.setEnabled(False)

        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())