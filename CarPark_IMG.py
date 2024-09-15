import pickle
import cv2

# img  = cv2.imread('carParkImg.png')
width, height = 107,48     #157-50, 240-190


# For drawing the existing Positions
try:
    with open('Parking_positions','rb') as f:
        poslist = pickle.load(f)
except:
    poslist = []



def Handle_Mouse(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        poslist.append((x,y))
    
    if events == cv2.EVENT_RBUTTONDOWN:
        
        for i,pos in enumerate(poslist):
            if pos[0]<x<pos[0]+width and pos[1]<y<pos[1]+height:
                poslist.pop(i)

    #storing Positions in a file
    with open('Parking_positions','wb') as f:
        pickle.dump(poslist, f)
        #logical error because when restarting the program all position would have erased so we dont want that
        #sol line ==> 8


while True: 
    img  = cv2.imread('carParkImg.png')
    for pos in poslist:
        x,y = pos
        cv2.rectangle(img, (x,y),(x+width,y+height),(255,0,255),2)

    
    # cv2.rectangle(img, (50,190),(157,240),(255,0,255),2)
    cv2.imshow("image",img)
    cv2.setMouseCallback('image', Handle_Mouse)

    cv2.waitKey(1)
    #4:22 62%