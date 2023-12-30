import cv2 as cv
import numpy as np
import os

# Chemin vers le dossier contenant les images
images_folder = 'video_crop'

# Liste pour stocker les images
image_list = []

# Charger les images dans la séquence
for image_file in sorted(os.listdir(images_folder)):
    if image_file.endswith('.png'):
        image_path = os.path.join(images_folder, image_file)
        image = cv.imread(image_path)
        image_list.append(image)

# Empiler les images en une seule structure de données
stacked_images = np.stack(image_list, axis=0)

# Calculer la médiane des images empilées
median_image = np.median(stacked_images, axis=0).astype(np.uint16)

# Afficher l'image médiane
median_image = (median_image.astype('float32') / 255 * 65535).astype('uint16')
cv.imwrite('ImageMediane.tif', median_image, [cv.IMWRITE_TIFF_COMPRESSION, 1])
