import cv2

def get_variance(image):
    #convert to greyscale
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #calculate the variance according with the laplacian of the image
    variance = cv2.Laplacian(grey, cv2.CV_64F, ksize=5).var()
    return variance