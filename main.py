import cv2 as cv
import ImageLoader
import Variance

images_path = "images/"
images = ImageLoader.load_images(images_path)

for image in images:
    image._variance = Variance.get_variance(image._cv , 120)
    print("variance:", image._variance)

images.sort(key=lambda x: x._variance, reverse=True)

for image in images:
    print(image._variance)