import string
from PIL import ImageDraw, ImageFont
from PIL.Image import new
import pandas as pd
import numpy as np
import random
import cv2 as cv
import math 
from skimage.util import random_noise
import tqdm

class Create_dataset:
    tmplt_text = 'F00/00      00:00\nV00/00\nA00A000' #Template text

    #Ta aqui pq eu fiz diferente e é isso
    def __init__(self):
        pass #Muito legal isso ai

    #Automatizing process
    def auto_generation(self):
        self.bg_collor = random.randint(105, 255)  # background color
        self.font_collor = random.randint(0, 50)  # font color
        self.blur = random.randint(1, 5)  # Randomize blur
        self.ond = random.randint(1, 7)  # Randomize n° ondulation
        self.angle = random.randint(1, 7)  # Randomize ondulation size
        self.noise = random.uniform(0, 0.7)  # Randomize noise mode
        
        #Calling functions in order to generate an unique image
        text = self.generate_random_text()
        img = self.create_img(text)
        img_converted = self.convert_pil_cv(img)
        img_blur = self.blur_img(img_converted)
        img_distorted = self.acceptable_noise(img_blur)
        img_edited = self.text_distortion(img_distorted)
        return img_edited, text
    
    #Randomize Text
    def generate_random_text(self):
        random_lote = ''.join(random.choice(string.ascii_uppercase) if char.isalpha() and char not in ["F", "V"] else char for char in self.tmplt_text) #Randomize alfa chars outside of F and V
        random_text = ''.join(random.choice(string.digits) if char.isdigit() else char for char in random_lote) #Randomize all numbers
        return random_text
    
    #Create image using PIL
    def create_img(self, text):
        img = new(mode="RGB", size=(500,130), color=(self.bg_collor, self.bg_collor, self.bg_collor)) #create canvas
        font = ImageFont.truetype("v4/assets/DotFontMatrix.ttf", 50) #font path & size
        draw = ImageDraw.Draw(img) #specify where to write
        draw.text((6,8), text, fill=(self.font_collor, self.font_collor, self.font_collor), font=font) #write text
        return img
    
    #Convert PIL to CV
    def convert_pil_cv(self, img_converted):
        img = img_converted
        img = img.convert("RGB") #Convert to RGB
        cv_img = np.array(img)  #Convert to array
        cv_img = cv_img[:, :, ::-1].copy() # Convert RGB to BGR
        return cv_img
    
    #Add blur
    def blur_img(self, img_converted):    
        img = cv.blur(img_converted,(self.blur, self.blur)) #Aplly blur
        return img

         
    #Add morfological distortion
    def text_distortion(self, img_blur):
        rows, cols, _ = img_blur.shape #Define image size
        img_output = np.zeros(img_blur.shape, dtype=img_blur.dtype) #Define output
        for n in range(rows):
            for j in range(cols):
                offset_x = 1 #Changing X axis pixel destination
                offset_y = int(self.ond * math.cos(self.angle * math.pi * j / 300)) #Changing Y axis pixel destination
                if n+offset_y < rows and j+offset_x < cols: #Check if the pixel is inside the original image
                    img_output[n,j] = img_blur[(n+offset_y)%rows,(j+offset_x)%cols] #Move pixel to destination
                else:
                    img_output[n,j] = 0 #If destination is outside of the original image set collor to black
        return img_output

    # Função para adicionar pontos aleatórios na imagem
    def acceptable_noise(self, img_distorted):
        gauss = np.random.normal(0,self.noise ,img_distorted.size) #Create an array with values between 0 and 0.5 with the same size of the image
        gauss = gauss.reshape(img_distorted.shape[0],img_distorted.shape[1],img_distorted.shape[2]).astype('uint8') #Shape de array accordinly with n° col and row of the image
        noise = img_distorted + img_distorted * gauss #Add noise
        return noise

labels = pd.DataFrame(columns=["id", "label"]) #Creating a Dataframe with the desirable columns

num_img = 100 #N° of images to be generated

with tqdm.tqdm(total=num_img) as pbar:
    for i in range(0,100):
        dataset_creator = Create_dataset() #Calling constructor
        img, text = dataset_creator.auto_generation() #Attributing the returns into img and text variables 
        text = text.replace("\n", "").replace(" ", "") #Normalizing text to be readable
        cv.imwrite(f"v4/assets/images/{i}.png",img) #Saving resulting image to path
        labels.loc[len(labels.index)] = [i, text] #Writing into dataframe the respective image ID and Ground Thruth
        pbar.update(1) #Updating progress bar

labels.to_csv("v4/labels.csv", index = False) #Save dataframe to latter use