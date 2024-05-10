import string
import os 
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import new
import pandas as pd
import numpy as np
import random
import cv2 as cv
import math 
from skimage.util import random_noise

#Template text
tmplt_text = 'F00/00      00:00\nV00/00\nA00A000'
#Background Colors
min_c_bg, max_c_bg = 105, 255
#Fonts Colors
min_c_font, max_c_font = 0, 50
#Blur variant
min_blur,max_blur = 1,5
#Text distortion number of ondulations variant
min_ond_numb, max_ond_numb = 2,7
#Text distortion angle of ondulations variant
min_angle, max_angle = 2,7

# Define texto para inserir na imagem
def generate_random_text():
    #randomiza os caracteres alfabéticos mantendom F:fabricação e V:validade
    random_lote = ''.join(random.choice(string.ascii_uppercase) if char.isalpha() and char not in ["F", "V"] else char for char in tmplt_text)
    #randomiza os números do texto (inclusive datas, mesmo que invalidas tem o intuíto de testar o maior número de combinações)
    random_text = ''.join(random.choice(string.digits) if char.isdigit() else char for char in random_lote)
    return random_text

def create_img():
    bg_color = random.randint(min_c_bg, max_c_bg) #background color
    font_color = random.randint(min_c_font, max_c_font) # font color
    img = new(mode="RGB", size=(500,130), color=(bg_color, bg_color, bg_color)) #create canvas
    font = ImageFont.truetype("v4/assets/DotFontMatrix.ttf", 50) #font path & size
    text = generate_random_text() #call function
    draw = ImageDraw.Draw(img) #specify where to write
    draw.text((6,8), text, fill=(font_color, font_color, font_color), font=font) #write text
    return img

def convert_pil_cv():
    img = create_img()
    img = img.convert("RGB") #Convert to RGB
    cv_img = np.array(img)  #Convert to array
    cv_img = cv_img[:, :, ::-1].copy() # Convert RGB to BGR
    return cv_img

def blur_img():    
    img = convert_pil_cv() 
    blur = random.randint(min_blur,max_blur) #Randomize blur
    img = cv.blur(img,(blur,blur)) #Aplly blur
    return img

def text_distortion():
    img = convert_pil_cv()
    ond = random.randint(min_ond_numb,max_ond_numb) #Randomize n° ondulation
    angle = random.randint(min_angle,max_angle) #Randomize ondulation size
    rows, cols, _ = img.shape #Define image size
    img_output = np.zeros(img.shape, dtype=img.dtype) #Define output
    for n in range(rows):
        for j in range(cols):
            offset_x = 1 #Changing X axis pixel destination
            offset_y = int(ond * math.cos(angle * math.pi * j / 300)) #Changing Y axis pixel destination
            if n+offset_y < rows and j+offset_x < cols: #Check if the pixel is inside the original image
                img_output[n,j] = img[(n+offset_y)%rows,(j+offset_x)%cols] #Move pixel to destination
            else:
                img_output[n,j] = 0 #If destination is outside of the original image set color to black
    return img_output

# Função para adicionar pontos aleatórios na imagem
def acceptable_noise():
    img = convert_pil_cv()
    mode = random.choice(["pepper", "gaussian"]) #Randomize noise mode
    skimage_img = cv.cvtColor(img, cv.COLOR_BGR2RGB) #Convert img to be readable by skimage
    noise_img = random_noise(skimage_img, mode=mode) #Apply noise mode
    return noise_img

# img = blur_img()
# img = text_distortion()
img = acceptable_noise()
cv.imshow("teste", img) 
blur_img()
cv.waitKey(0)



