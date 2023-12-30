import cv2 as cv
import numpy as np
import imutils

def align_frames_fast(frames, frames_index, path, amount):
    video = cv.VideoCapture(path)
    for i in range(amount):
        video.set(cv.CAP_PROP_POS_FRAMES, frames_index[i])
        ret, image = video.read()
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
  
  
        # Applying the function
        fast = cv.FastFeatureDetector_create()
        fast.setNonmaxSuppression(False)
        
        
        # Drawing the keypoints
        kp = fast.detect(gray_image, None)
        kp_image = cv.drawKeypoints(image, kp, None, color=(0, 255, 0))
        
        cv.imshow('FAST', kp_image)
        k = cv.waitKey(25)
        if k == 27:
            break
    cv.destroyAllWindows()

def align_frames_brief(frames, frames_index, path, amount):
    video = cv.VideoCapture(path)
    for i in range(amount):
        video.set(cv.CAP_PROP_POS_FRAMES, frames_index[i])
        ret, image = video.read()
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        # Applying the function
        fast = cv.FastFeatureDetector_create()
        brief = cv.xfeatures2d.BriefDescriptorExtractor_create()

        test_keypoints = fast.detect(gray_image, None)
        test_keypoints, test_descriptor = brief.compute(gray_image, test_keypoints)

        #kp, des = brief .detectAndCompute(gray_image, None)
        
        
        # Applying the function
        kp_image = cv.drawKeypoints(image, test_keypoints, None, color=(0, 255, 0), flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv.imshow('SIFT', kp_image)
        k = cv.waitKey(25)
        if k == 27:
            break
    cv.destroyAllWindows()

def align_frames_sift(frames, frames_index, path, amount):
    video = cv.VideoCapture(path)

    for i in range(amount):
        video.set(cv.CAP_PROP_POS_FRAMES, frames_index[i])
        ret, image = video.read()
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        # Applying the function
        sift = cv.SIFT.create(
            nfeatures = 2000,
            #nOctaveLayers = 3,
            contrastThreshold = 0.005,
            edgeThreshold = 100
        )
        kp, des = sift.detectAndCompute(gray_image, None)
        
        
        # Applying the function
        kp_image = cv.drawKeypoints(image, kp, None, color=(0, 255, 0), flags=0)
        cv.imshow('SIFT', kp_image)
        k = cv.waitKey(25)
        if k == 27:
            break
    cv.destroyAllWindows()

def align_frames_orb(frames, frames_index, path, amount):
    video = cv.VideoCapture(path)
    feature_params = dict(
        scaleFactor=1.2,  # Facteur d'échelle entre les niveaux de l'octave
        nlevels=8,        # Nombre de niveaux d'échelle dans chaque octave
        edgeThreshold=5,  # Seuil pour rejeter les bords
        patchSize=31,     # Taille du patch pour la description
        nfeatures=2000.0
    )
    for i in range(amount):
        video.set(cv.CAP_PROP_POS_FRAMES, frames_index[i])
        ret, image = video.read()
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        # Applying the function
        orb = cv.ORB_create(
            scaleFactor=1.2,  # Facteur d'échelle entre les niveaux de l'octave
            nlevels=8,        # Nombre de niveaux d'échelle dans chaque octave
            edgeThreshold=5,  # Seuil pour rejeter les bords
            patchSize=31,     # Taille du patch pour la description
            nfeatures=2000
        )
        kp, des = orb.detectAndCompute(gray_image, None)
        
        # Drawing the keypoints
        kp_image = cv.drawKeypoints(image, kp, None, color=(0, 255, 0), flags=0)
        
        cv.imshow('ORB', kp_image)

        k = cv.waitKey(25)
        if k == 27:
            break
    cv.destroyAllWindows()

def align_frames(frames, frames_index, path, amount):
    video = cv.VideoCapture(path)
    _max_corners = 1000
    feature_params = dict(maxCorners = _max_corners, qualityLevel = 0.01, minDistance = 7, blockSize = 7)

    lk_params = dict(winSize = (15, 15), maxLevel = 2, criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

    color = np.random.randint(0, 255, (_max_corners, 3))

    video.set(cv.CAP_PROP_POS_FRAMES, frames_index[0])
    ret, frame = video.read()

    old_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    p0 = cv.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

    mask = np.zeros_like(frame)

    for i in range(1, amount):
        old_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        video.set(cv.CAP_PROP_POS_FRAMES, frames_index[i])
        ret, frame = video.read()
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
        # calculate optical flow
        p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    
        # Select good points
        good_new = p1[st == 1]
        good_old = p0[st == 1]
    
        # draw the tracks
        for i, (new, old) in enumerate(zip(good_new, 
                                        good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)),
                            color[i].tolist(), 2)
            
            frame = cv.circle(frame, (int(a), int(b)), 5,
                            color[i].tolist(), 1)
            
        img = frame
    
        cv.imshow('frame', img)
        
        k = cv.waitKey(25)
        if k == 27:
            break
    
        # Updating Previous frame and points 
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)
    
    cv.destroyAllWindows()


def align_images1(image, template, maxFeatures, keepPercent, debug=False):
    imageGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    templateGray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

    orb = cv.ORB_create(
        #scaleFactor=1.2,  # Facteur d'échelle entre les niveaux de l'octave
        #nlevels=8,        # Nombre de niveaux d'échelle dans chaque octave
        #edgeThreshold=5,  # Seuil pour rejeter les bords
        #patchSize=31,     # Taille du patch pour la description
        nfeatures=2000
    )
    (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
    (kpsB, descsB) = orb.detectAndCompute(templateGray, None)

    method = cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    matcher = cv.DescriptorMatcher_create(method)
    matches = matcher.match(descsA, descsB, None)

    matches = sorted(matches, key=lambda x:x.distance)
    keep = int(len(matches) * keepPercent)
    matches = matches[:keep]

    if debug:
        matchedVis = cv.drawMatches(image, kpsA, template, kpsB, matches, None)
        matchedVis = imutils.resize(matchedVis, width=1000)
        cv.imshow("", matchedVis)
        cv.waitKey(0)

    ptsA = np.zeros((len(matches), 2), dtype="float")
    ptsB = np.zeros((len(matches), 2), dtype="float")

    for (i, m) in enumerate(matches):
        ptsA[i] = kpsA[m.queryIdx].pt
        ptsB[i] = kpsB[m.trainIdx].pt

    (H, mask) = cv.findHomography(ptsA, ptsB, method=cv.RANSAC, ransacReprojThreshold=5.0)
    (h, w) = template.shape[:2]
    aligned = cv.warpPerspective(image, H, (w, h))
    return aligned

def align_images(image, template, maxFeatures, keepPercent, debug=False):
    image_reference = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    image_to_align = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Créer l'extracteur SURF
    sift = cv.SIFT_create()

    # Trouver les keypoints et descripteurs
    keypoints_ref, descriptors_ref = sift.detectAndCompute(image_reference, None)
    keypoints_align, descriptors_align = sift.detectAndCompute(image_to_align, None)

    # Trouver les correspondances
    matcher = cv.FlannBasedMatcher()
    matches = matcher.knnMatch(descriptors_ref, descriptors_align, k=2)

    # Filtrer les correspondances
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Calculer la transformation
    if len(good_matches) > 10:
        src_pts = np.float32([keypoints_ref[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints_align[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        transformation_matrix, mask = cv.findHomography(dst_pts, src_pts, cv.RANSAC, 5.0)
        
        # Appliquer la transformation
        aligned_image = cv.warpPerspective(image, transformation_matrix, (image_reference.shape[1], image_reference.shape[0]))
        return True, aligned_image
    else:
        #cannot match target image with reference image
        return False, None