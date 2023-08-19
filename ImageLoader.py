import os
import cv2 as cv

class Image:
    def __init__(self, _cv, _path):
        self._cv = _cv  #stores the data provided by the cv.imread() function
        self._variance = 0
        self._path = _path

#create a list of Image objects
def load_images(directory):
    images = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            cv_img = cv.imread(directory + file)
            images.append(Image(cv_img, directory + file))
    return images