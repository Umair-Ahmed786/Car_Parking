import cv2
import cvzone
import numpy as np
import pickle

#video 
video = cv2.VideoCapture('carPark.mp4')

with open('Parking_positions','rb') as f:
        posList = pickle.load(f)    

width, height = 107, 48  

def Crop(imgProcess):
    spaceCount = 0
     
    for pos in posList:
          
        x,y = pos
        imgCrop = imgProcess[y: y + height, x: x + width]

        #   cv2.imshow(str(x + y),imgCrop)
        count = cv2.countNonZero(imgCrop)

        if count < 900: #no car detected #green
                color = (0,255,0)
                thickness = 3
                spaceCount+=1
        else:
                color = (0,0,255)
                thickness = 2
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=(0,0,255))
        cv2.rectangle(img, pos, (x+width, y+height), color, thickness)
    

    #Printing the Total Vehicle counts
    cvzone.putTextRect(img, f'Free: {spaceCount}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(0,200,0))

           
    
while True:

    if video.get(cv2.CAP_PROP_POS_FRAMES) == video.get(cv2.CAP_PROP_FRAME_COUNT):
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success,img = video.read()

#Preprocessing Images:

    imggrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #for reducing image noise and detail
    imgBlur = cv2.GaussianBlur(imggrey, (3,3), 1)

    #for converting image to binary image with black and white pixels only
    imgThresh = cv2.adaptiveThreshold(imggrey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    
    #for reducing image noice by removing extra white pixels
    imgMedian = cv2.medianBlur(imgThresh, 5)
    
    #optional For making the white pixel thicker
    kernel = np.ones((2, 2), np.uint8)
    imgDilate  = cv2.dilate(imgMedian, kernel, 1)

#Croping the parts of Images
    Crop(imgDilate)

#Printing the rectangles on Images    
    # for pos in posList:
    #     x,y = pos
    #     cv2.rectangle(img, pos, (x+width, y+height), (0,0,255), 2)
    
#displaying the images
    cv2.imshow('Image',img)
    # cv2.imshow('grey',imggrey)
    # cv2.imshow('blur',imgBlur)
    # cv2.imshow('threshold',imgThresh)
    # cv2.imshow('imgMedian',imgMedian)
    # cv2.imshow('imgDilate',imgDilate)
    
    cv2.waitKey(10)