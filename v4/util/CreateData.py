import string
import os 
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import new
import pandas as pd
import numpy as np
import random
import cv2 as cv

#Background Colors
min_c_bg, max_c_bg = 105, 255
#Fonts Colors
min_c_font, max_c_font = 0, 50
#Blur variant
min_blur,max_blur = 1,5

# Define texto para inserir na imagem
def generate_random_text():
    #template do texto a ser gerado
    datas = 'F00/00      00:00\nV00/00\nA00A000'
    #randomiza os caracteres alfabéticos mantendom F:fabricação e V:validade
    random_lote = ''.join(random.choice(string.ascii_uppercase) if char.isalpha() and char not in ["F", "V"] else char for char in datas)
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
    # img.show() #show img
    return img

def convert_pil_cv():
    img = create_img()
    img = img.convert("RGB")
    cv_img = np.array(img)  
    cv_img = cv_img[:, :, ::-1].copy() # Convert RGB to BGR
    return cv_img

def blur_img():    
    img = convert_pil_cv()
    blur = random.randint(min_blur,max_blur)
    img = cv.blur(img,(blur,blur))
    return img






img = blur_img()
cv.imshow("teste", img) 
blur_img()
cv.waitKey(0)



