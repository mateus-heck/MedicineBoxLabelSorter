import string
from PIL import ImageDraw, ImageFont
from PIL.Image import new
import cv2
import numpy as np

letters = [char for char in string.ascii_uppercase] #Template text
digits = [char for char in string.digits] #Template text
possible_digits = [char for char in [letters + digits + ["/"] + [":"]]][0] #Template text
possible_fonts = ['DFM.ttf', 'DFM_italic.ttf']
bg_collor = (255,255,255)  # background color
font_collor = (0, 0, 0)  # font color
kernel = np.full((3, 3 ), -1) #Distortion kernel variable

#Create image using PIL
def create_img(text, font):
    img = new(mode="RGB", size=(300,300), color=(bg_collor)) #create canvas
    font = ImageFont.truetype(f"v4/assets/{font}", 400) #font path & size
    draw = ImageDraw.Draw(img) #specify where to write
    draw.text((20,10), text, fill=(font_collor), font=font) #write text
    img = img.convert("RGB") #Convert to RGB
    cv_img = np.array(img)  #Convert to array
    cv_img = cv_img[:, :, ::-1].copy() # Convert RGB to BGR
    img = cv2.dilate(cv_img, kernel, iterations=8) #Apply negative dilatation 
    return img

for i in possible_fonts: #iterate over fonts
    font = i #font path
    for j in possible_digits: #iterate over digits
        img = create_img(j, font) #create image
        if j == ":": #replace special characters
            j = "dots" 
        elif j == "/": 
            j = "slash"
        if i == "DFM_italic.ttf":  #font type
            font_type = "italic" 
        else: 
            font_type = "regular"
        cv2.imwrite(f"v4/assets/single_digits/{font_type}/{j}.png", img) #save image
