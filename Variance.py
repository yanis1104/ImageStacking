import cv2 as cv

def get_variance(image, threshold):
    #convert to greyscale
    grey = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    #calculate the variance according with the laplacian of the image
    variance = cv.Laplacian(grey, cv.CV_64F).var()
    return variance