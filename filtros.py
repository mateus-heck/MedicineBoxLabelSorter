import cv2
import numpy as np
import matplotlib.pyplot as plt
import imgaug.augmenters as iaa

imagem = cv2.imread('img3.png')

def sharpen(img):
  sharpen = iaa.Sharpen(alpha=1.0, lightness = 1.0)
  sharpen_img = sharpen.augment_image(img)
  return sharpen_img

sharpened_image = sharpen(imagem)
_, binary_image = cv2.threshold(sharpened_image, 1, 255, cv2.THRESH_BINARY)

thresh = cv2.threshold(binary_image, 115, 255, cv2.THRESH_BINARY_INV)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,2)) #Mexer aqui
dilate_2 = cv2.dilate(thresh, kernel, iterations=1)
final = cv2.threshold(dilate_2, 115, 255, cv2.THRESH_BINARY_INV)[1]

plt.imshow(cv2.cvtColor(final, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

cv2.imwrite('img_tratada.png', final)
