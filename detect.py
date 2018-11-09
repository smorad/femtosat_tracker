import numpy as np
import cv2

def load_img(fname):
    frame = cv2.imread(fname)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def find_contours(frame):
    ret, thresh = cv2.threshold(frame, 40, 255, cv2.THRESH_BINARY)
    frame2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        moments = cv2.moments(contours[0])
        center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))
    except Exception:
        return None, None
    return contours, center


def display_contours(frame, contours, distance=0):
    # draw contours
    cv2.namedWindow('contours', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('contours', 640, 480)
    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    try:
        moments = cv2.moments(contours[0])
        center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))
    except Exception:
        cv2.imshow('contours', frame)
        return

    contour_frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
    cv2.circle(contour_frame, center, 1, (0, 255, 0), -1)
    cv2.putText(contour_frame, str(distance), (10,80), font, 1, (255, 255, 255))
    cv2.imshow('contours', contour_frame)
    cv2.waitKey(100)


if __name__ == '__main__':
    fname = '/home/smorad/Pictures/depth_test.png'
    frame = load_img(fname)
    contours, center = find_contours(frame)
    display_contours(frame, contours)
