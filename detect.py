import numpy as np
import cv2

def load_img(fname):
    frame = cv2.imread(fname)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def find_contours(frame):
    center = None
    ret, thresh = cv2.threshold(frame, 45, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # ensure only one contour
        contours = [sorted(contours, key=cv2.contourArea, reverse=True)[0]]
        moments = cv2.moments(contours[0])
        if all([int(moments["m10"]), int(moments["m00"]), int(moments["m01"])]):
            center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))
        return contours, center

    print('No contours found')
    return None, None


def display_contours(frame, contours, distance=0):
    # draw contours
    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    try:
        moments = cv2.moments(contours[0])
        center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))
    except Exception:
        cv2.imshow('contours', frame)
        return

    cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
    cv2.circle(frame, center, 1, (0, 255, 0), -1)
    cv2.putText(frame, str(distance), (10,80), font, 1, (255, 255, 255))
    cv2.imshow('contours', frame)
    cv2.waitKey(100)


def init_cv2():
    cv2.namedWindow('contours', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('contours', 640, 480)

if __name__ == '__main__':
    fname = '/home/smorad/Pictures/depth_test.png'
    frame = load_img(fname)
    contours, center = find_contours(frame)
    display_contours(frame, contours)
