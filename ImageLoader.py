import os
import cv2 as cv
import numpy as np
import Variance
from Clock import Clock
import time

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

#def load_video(path):
#    video = cv.VideoCapture(path)
#    return video

def run_video(video):
    while (video.isOpened()):
        ret, frame = video.read()
        #frame = cv.resize(frame, (624, 360), fx = 0, fy = 0, interpolation = cv.INTER_CUBIC)
        cv.imshow('Frame', frame)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break

def analyse_video(path):
    video = cv.VideoCapture(path)
    frames = {}
    frame_index = 0
    while(True):
        ret, frame = video.read()
        if ret:
            variance = Variance.get_variance(frame)
            frames[frame_index] = variance
            frame_index += 1
        else:
            break
    return frames

def sort_index_frames_by_variance(frames):
    sorted_frames_with_variance = sorted(frames.items(), key=lambda item: item[1], reverse=True)
    sorted_key_frames = []
    for frame in sorted_frames_with_variance:
        sorted_key_frames.append(frame[0])
    return sorted_frames_with_variance, sorted_key_frames

def nothing(x):
    pass

def create_trackbar(frames_index, video_path):
    clock = Clock()

    video = cv.VideoCapture(video_path)
    cv.namedWindow('Sorted frames')

    cv.createTrackbar('Frame', 'Sorted frames', 0, len(frames_index) - 1, nothing)
    previous_trackbar_pos = 0
    trackbar_pos = 0
    #cv.setTrackbarPos('Frame', "Sorted frames", frames_index[trackbar_pos])
    video.set(cv.CAP_PROP_POS_FRAMES, frames_index[trackbar_pos])
    ret, frame = video.read()
    while(1):
        if clock.get_time_as_millisecond() >= 50:
            clock.restart()
            if ret == True:
                cv.imshow('Sorted frames', frame)
            k = cv.waitKey(1) & 0xFF
            if k == 27:
                break
            trackbar_pos = cv.getTrackbarPos('Frame', 'Sorted frames')
            if previous_trackbar_pos != trackbar_pos:
                video.set(cv.CAP_PROP_POS_FRAMES, frames_index[trackbar_pos])
                ret, frame = video.read()
                previous_trackbar_pos = trackbar_pos
    cv.destroyAllWindows()