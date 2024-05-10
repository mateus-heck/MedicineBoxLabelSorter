import string
import os 
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import new
import pandas as pd
import numpy as np
import random
import cv2

#Cores Background
min_c_bg = 105
max_c_bg = 255
#Cores Fonte
min_c_font = 0
max_c_font = 50

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
    bg_color = random.randint(min_c_bg, max_c_bg)
    font_color = random.randint(min_c_font, max_c_font)
    img = new(mode="RGB", size=(500,130), color=(bg_color, bg_color, bg_color))
    font = ImageFont.truetype("v4/assets/DotFontMatrix.ttf", 50)
    text = generate_random_text() 
    draw = ImageDraw.Draw(img)
    draw.text((6,8), text, fill=(font_color, font_color, font_color), font=font)
    img.show()
create_img()

# def apply_skewing(random_text):


