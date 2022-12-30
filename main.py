import cv2 as cv ## 4.5.5.64

from rembg import remove ## 2.0.30

import numpy as np ## 1.23.5


def subs(image,crop):
    
    # Grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    # finding thresold ---> as bcakground is 0 we take range from 1 to 255
    # thresh = bin mask
    ret, thresh = cv.threshold(gray, 1, 255, cv.THRESH_BINARY)
    
    # Finding Contours
    
    contours, hierarchy = cv.findContours(thresh, 
        cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    
    
    
    # getting maximum contours from all the detected contours , so inner details of subject is not shown
    
    if len(contours) != 0:
        # draw in  the contours that were founded
        cv.drawContours(crop, contours, -1, 255, 3)

        # find the biggest countour  by the area
        c = max(contours, key = cv.contourArea)
    

    
    # Draw all contours
    # -1 signifies drawing all contours
    cv.drawContours(crop, contours, -1, (0, 255, 0), 3)
    
    return crop

def mainf():

    # add the path here 

    path = input('give path of the file : ')

    # image read and resizing 

    img = cv.imread(path)
    
    # resizing size can be arbitrary

    img = cv.resize(img,(1024,725))

    # usage of selectROI for bounding box selection

    img_bbox = cv.selectROI(img)
    
    cv.destroyAllWindows()
    
    # we get the croped image using indexing of original image with rectangular coordinated of bounding box drawn by the user

    croped = img[int(img_bbox[1]):int(img_bbox[1]+img_bbox[3]), int(img_bbox[0]):int(img_bbox[0]+img_bbox[2])]

    bgless = remove(croped)
    
    ## function 
    bgless = subs(bgless,croped)
   
    ind = list(img_bbox)

    # rescalling outline image to original image 
    bgless = cv.resize(bgless,(ind[2],ind[3]))

    # overlayying
    imgc = img
    imgc[int(ind[1]):int(ind[1]+ind[3]),int(ind[0]):int(ind[0]+ind[2])] = bgless
    cv.imwrite(f'{path[0]}+res.jpg',imgc)
    # orginal image may got changed during the process of re-initialization
    img = cv.imread(path)
    img = cv.resize(img,(1024,725))
    
    #UI
    flag = 0
    while 1:
        if flag== 0:
            
            cv.imshow('outline',imgc)
        else:
            
            cv.imshow('original image',img) 
            
        k = cv.waitKey(1) & 0xFF
        if k == ord('c'):
            if flag==0:
                flag = 1
                cv.destroyAllWindows()
            else:
                flag = 0
                cv.destroyAllWindows()
        if k == ord('q'):
            break  
    cv.destroyAllWindows()

#UI
f = 0
while 1:
    mainf()
    f = int(input("\nif you want to end the program please press -1 else 0 : "))
    if f == -1:
        break
print("end of the function execution")


