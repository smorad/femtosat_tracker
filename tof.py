import Voxel
import numpy as np
from detect import *

def createWindow():
    global window
    if window == None:
        window = MainWindow(cameraSystem)
    return

class MainWindow():
        ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
        # self.width = 80
 #  self.height = 60
        def __init__(self, cameraSystem):
                print("MainWindow init")
                self.depthCamera = cameraSystem.connect(devices[0])
                rate = Voxel.FrameRate()
                rate.numerator = 10
                rate.denominator = 1
                self.depthCamera.setFrameRate(rate)
                if self.depthCamera:
                        self.depthCamera.clearAllCallbacks()
                        self.depthCamera.registerCallback(Voxel.DepthCamera.FRAME_DEPTH_FRAME, self.callbackInternal)
                        #self.depthCamera.registerCallback(Voxel.DepthCamera.FRAME_XYZI_POINT_CLOUD_FRAME, self.callbackInternal)
                        if not self.depthCamera.start():
                                print(" start fail")
                        else:
                                print(" start ok")
                
        def callbackInternal(self, depthCamera, frame, type):
                #print("frame.id:  %s" %frame.id)   
                #print("frame.id:  %s" %frame.timestamp)   
                #print('frame.id type : %s' %type)
                amp, depth = self.to_cv2(frame)
                contours, center = find_contours(amp)
                if center:
                    distance = depth[center[0], center[1]]
                    print('dist2tgt:', distance, center)
                    display_contours(amp, contours, distance)
                else:
                    display_contours(amp, contours)

                #print('distance: ', depth[center[0], center[1]])
        
        def to_cv2(self, frame):
                # frames of size 60x60
                #h_px = 80
                #v_px = 60
                data_frame = Voxel.DepthFrame.typeCast(frame)
                #print('frame size: ', data_frame.size.width, data_frame.size.height) 
                # 80x60
                width_px = data_frame.size.width
                height_px = data_frame.size.height
                amp_frame = np.ndarray([height_px, width_px], dtype=np.uint8)
                depth_frame = np.ndarray([height_px, width_px], dtype=float)
                #print('ranges: ', range(width_px), range(height_px))
                for x in range(width_px):
                        for y in range(height_px):
                                #print('reading px ', y * (width_px) + x, x, y)
                                amp_frame[y, x] = int(254 * data_frame.amplitude[y * width_px + x])
                                depth_frame[y, x] = data_frame.depth[y * width_px + x]
                
                #print(amp_frame, depth_frame)
                #cv2.imshow('amp', amp_frame)
                #cv2.waitKey(1)
                return cv2.flip(cv2.flip(amp_frame, 0), 1), cv2.flip(cv2.flip(depth_frame, 0), 1)
                

                


cameraSystem = Voxel.CameraSystem()

devices = cameraSystem.scan()
# depthCamera = None

if len(devices) == 1:
         print(" find one devices")      
         window = MainWindow(cameraSystem)
         key = raw_input("Input enter key to quit ")
         print(" quit now")
else:
   print(" no device found")


del cameraSystem
