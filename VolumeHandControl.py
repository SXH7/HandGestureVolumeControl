import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import handTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wcam, hcam = 640, 480

cap = cv.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

ptime = 0

detector = htm.handDetector()



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#volume.GetMute()
#volume.GetMasterVolumeLevel()

volRange = volume.GetVolumeRange()


minVol = volRange[0]
maxVol = volRange[1]





while True:

    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv.circle(img, (x1, y1), 15, (255, 0, 255), cv.FILLED)
        cv.circle(img, (x2, y2), 15, (255, 0, 255), cv.FILLED)

        cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        #print(length)

        # hand range 20 200
        # volume range -65 0

        volumex = np.interp(length, [20, 200], [minVol, maxVol])
        print(volumex)
        volume.SetMasterVolumeLevel(volumex, None)



        if (length<50):
            cv.circle(img, (cx, cy), 15, (0, 255, 0), cv.FILLED)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime

    cv.putText(img, str(int(fps)), (20, 50), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv.imshow('Video', img)
    cv.waitKey(10)
