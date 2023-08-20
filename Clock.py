import cv2 as cv

class Clock:
    def __init__(self):
        self.t1 = cv.getTickCount()
        self.t2 = 0

    def get_time_as_millisecond(self):
        self.t2 = cv.getTickCount()
        time_ms = (self.t2 - self.t1) / cv.getTickFrequency()
        return time_ms * 1000
        
    def restart(self):
        self.t1 = cv.getTickCount()
        self.t2 = 0