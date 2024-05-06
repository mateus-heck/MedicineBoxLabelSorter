import cv2
import moviepy.editor as mp
import os

# Definir as variáveis
n_imagens_boas = 10  # Número de imagens boas
n_imagens_ruins = 10  # Número de imagens ruins
fps = 24  # Taxa de quadros por segundo
duracao_video_total = 20  # Duração do vídeo em segundos
duracao_video_indv = 1 # Duração de cada clipe

# Carregar as imagens
imagens_boas = [cv2.imread("MedicineBoxLabelSorter/Generator/Good/"+imagem) for imagem in os.listdir('MedicineBoxLabelSorter/Generator/Good')]
imagens_ruins = [cv2.imread("MedicineBoxLabelSorter/Generator/Bad/"+imagem) for imagem in os.listdir('MedicineBoxLabelSorter/Generator/Bad')]

# Criar clipes de vídeo para imagens boas
clips_boas = [(mp.ImageClip(img).set_duration(0.1)) for img in imagens_boas]

concat_clip = [mp.CompositeVideoClip([clip.fx( mp.transfx.slide_out, 0.1, 'left')]) for clip in clips_boas]
concat_clip = mp.concatenate_videoclips(concat_clip)
concat_clip.write_videofile("MedicineBoxLabelSorter/Generator/videos/Final.mp4", fps=24)
