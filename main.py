import cv2 as cv
import ImageLoader

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

ImageLoader.create_trackbar(frames_index, path)