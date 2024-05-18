import cv2 as cv
import numpy as np

img = cv.imread('v4/assets/real_imgs/1.jpg')
img = cv.copyMakeBorder(img, 100, 100, 100, 100, cv.BORDER_CONSTANT, value=(255,255,255))
# cv.imshow('img', img)
# cv.waitKey(0)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
range = cv.inRange(gray, 0, 100)
# cv.imshow('range', range)
# cv.waitKey(0)
blur = cv.GaussianBlur(range, (5, 5), 0)
# cv.imshow('blur', blur)
# cv.waitKey(0)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (50, 5))
dilate = cv.dilate(blur, kernel, iterations=5)
cv.imshow('dilate', dilate)
cv.waitKey(0)

contours, hierarchy = cv.findContours(dilate, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv.contourArea, reverse=True)
largest = contours[0]
minArea = cv.minAreaRect(largest)
box = cv.boxPoints(minArea)
box = np.intp(box)
box_img = dilate.copy()
cv.drawContours(box_img, [box], 0, (255, 255, 255), 3)
# cv.imshow('imgaa', box_img)
# cv.waitKey(0)

def crop_image(rect, image):
    shape = (image.shape[1], image.shape[0])  # cv2.warpAffine expects shape in (length, height)
    center, size, theta = rect
    width, height = tuple(map(int, size))
    center = tuple(map(int, center))
    if width < height:
        theta -= 90
        width, height = height, width

    matrix = cv.getRotationMatrix2D(center=center, angle=theta, scale=1.0)
    image = cv.warpAffine(src=image, M=matrix, dsize=shape)

    x = int(center[0] - width // 2)
    y = int(center[1] - height // 2)

    image = image[y : y + height, x : x + width]

    return image

image = crop_image(minArea, blur)
# cv.imshow('ss', image)
# cv.waitKey(0)
text_height = image.shape[0]//3
length = image.shape[1]
# print(text_height)
img_1 = image[0:text_height, 0:length]
img_1 = cv.copyMakeBorder(img_1, 100, 100, 100, 100, cv.BORDER_CONSTANT, value=0)
# cv.imshow('img_1', img_1)
# cv.waitKey(0)
img_2 = image[text_height:text_height*2, 0:length]
img_2 = cv.copyMakeBorder(img_2, 100, 100, 100, 100, cv.BORDER_CONSTANT, value=0)
# cv.imshow('img_2', img_2)
# cv.waitKey(0)
img_3 = image[text_height*2:text_height*3, 0:length]
img_3 = cv.copyMakeBorder(img_3, 100, 100, 100, 100, cv.BORDER_CONSTANT, value=0)
# cv.imshow('img_3', img_3)
# cv.waitKey(0)


dilate_3 = cv.dilate(img_3, kernel, iterations=2)
# cv.imshow('dilate_3', dilate_3)
# cv.waitKey(0)

# Find (x,y) and (x, y+h) to warpperspective
contours, hierarchy = cv.findContours(dilate_3, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
x, y, w, h = cv.boundingRect(contours[0])
rec_x1, rec_y1, rec_x2, rec_y2 = x, y, x, y+h

for contour in contours:
    approx = cv.approxPolyDP(contour, 0.02*cv.arcLength(contour, True), True)
    # cv.drawContours(img_3, [approx],0, (255, 255, 255), 3)
    approx = sorted(approx, key=lambda x: x[0][0])
    if approx[0][0][1] < approx[1][0][1]:
        angular_x1, angular_y1, angular_x2, angular_y2 = approx[0][0][0], approx[0][0][1], approx[1][0][0], approx[1][0][1]
    else:
        angular_x1, angular_y1, angular_x2, angular_y2 = approx[1][0][0], approx[1][0][1], approx[0][0][0], approx[0][0][1]
    # print(angular_x1, angular_y1, angular_x2, angular_y2)
#Get the tilt of first letter
aux = abs(rec_x1 - angular_x1)

pts1 = np.float32([[angular_x1, angular_y1], [angular_x2, angular_y2],
                   [x+w, y], [x+w - aux, y+h]])
pts2 = np.float32([[rec_x1, rec_y1], [rec_x2, rec_y2],
                   [x+w, y], [x+w, y+h]])

matrix = cv.getPerspectiveTransform(pts1, pts2)

#1
result_1 = cv.warpPerspective(img_1, matrix, (img_1.shape[1], img_1.shape[0]))
result_1 = result_1[95:-95, 145:-145]
result_1 = cv.resize(result_1,(0,0), fx=2, fy=2)
cv.imshow('result_1', result_1)
cv.waitKey(0)
#2
result_2 = cv.warpPerspective(img_2, matrix, (img_2.shape[1], img_2.shape[0]))
result_2 = result_2[95:-95, 145:-145]
result_2 = cv.resize(result_2,(0,0), fx=2, fy=2)
cv.imshow('result_2', result_2)
cv.waitKey(0)
#3
result_3 = cv.warpPerspective(img_3, matrix, (img_3.shape[1], img_3.shape[0]))
result_3 = result_3[95:-95, 145:-145]
result_3 = cv.resize(result_3,(0,0), fx=2, fy=2)
cv.imshow('result_3', result_3)
cv.waitKey(0)

