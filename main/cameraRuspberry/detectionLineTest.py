import cv2
import numpy as np
import time

#пока тут тест детекции линии

def countError(img): 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    up_line = 1000
    down_line = 1020
    croped_gray = gray[:][up_line:down_line]
    _, thresh = cv2.threshold(croped_gray, 70, 255, cv2.THRESH_BINARY_INV)
    
    C = cv2.moments(thresh,1)
   
    if C['m00'] > 1:
        x = int(C['m10'] / C['m00'])
        y = int(C['m01']/ C['m00'])
        cv2.circle(croped_gray, (x, y), 10, (255,255,255), -1)
        error = croped_gray.shape[1] // 2 - x 
        return error

    
    return 0
    
def main():
    cam = cv2.VideoCapture("test.mp4")

    tic = time.time()
    iter1 = 0
    while(cam.isOpened() and (time.time() - tic) < 5):
        ret, frame = cam.read()
        if ret == True:
            countError(frame)
            #cv2.imshow("result", result)
            #cv2.waitKey(1)
            pass
        else:
            break

        iter1 += 1
    toc = time.time()

    print("dtime", 1/30 - (toc-tic)/iter1)
          


if __name__ == "__main__":
     main()
    