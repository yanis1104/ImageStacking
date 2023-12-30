import cv2 as cv
import ImageLoader
import ImageAlignment

path = 'videos/video_crop.ser'

frames = ImageLoader.analyse_video(path)
# frames is a dict which associates the index of a frame to its variance. The dict is then sorted by highest variance
# frames_index is a list that stores the index of the frames sorted previously 
frames, frames_index = ImageLoader.sort_index_frames_by_variance(frames)

#for frame in frames:
#    print(frame)
#print("########")
#for frame in frames_index:
#    print(frame)

#ImageLoader.create_trackbar(frames_index, path)
print(frames[frames_index[0]][0])
#ImageAlignment.align_frames_sift(frames, frames_index, path, 1000)
###################
ksize = (5, 5)
video = cv.VideoCapture(path)
video.set(cv.CAP_PROP_POS_FRAMES, frames_index[0])
ret_template, template = video.read()

video.set(cv.CAP_PROP_POS_FRAMES, frames_index[1])
ret_image, image = video.read()

cv.imwrite("template.png", template)
cv.imwrite("target.png", image)

template = cv.GaussianBlur(template, ksize, cv.BORDER_DEFAULT)
image = cv.GaussianBlur(image, ksize, cv.BORDER_DEFAULT)

stat, image_aligned = ImageAlignment.align_images(image, template, 1000, 0.5, True)

cv.destroyAllWindows()
if stat:
    cv.imwrite("image_template.png", template)
    cv.imwrite("image_aligned.png", image_aligned)