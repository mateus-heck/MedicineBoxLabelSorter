import cv2
import moviepy.editor as mp
import os
import moviepy.video.compositing.transitions as transfx
from moviepy.decorators import requires_duration
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import ImageClip
# Definir as variáveis
n_imagens_boas = 10  # Número de imagens boas
n_imagens_ruins = 10  # Número de imagens ruins
fps = 24  # Taxa de quadros por segundo
duracao_video = 5  # Duração do vídeo em segundos


# Carregar as imagens
imagens_boas = [cv2.imread("MedicineBoxLabelSorter/Good/"+imagem) for imagem in os.listdir('MedicineBoxLabelSorter/Good')]
imagens_ruins = [cv2.imread("MedicineBoxLabelSorter/Bad/"+imagem) for imagem in os.listdir('MedicineBoxLabelSorter/Bad')]

# Processamento das imagens boas
imagens_boas_processadas = []
for imagem in imagens_boas:
    # Aplique o processamento desejado à imagem aqui (redimensionamento, rotação, etc.)
    imagem_processada = imagem  # Exemplo: sem processamento
    imagens_boas_processadas.append(imagem_processada)

# Processamento das imagens ruins
imagens_ruins_processadas = []
for imagem in imagens_ruins:
    # Aplique o processamento desejado à imagem aqui (redimensionamento, rotação, etc.)
    imagem_processada = imagem  # Exemplo: sem processamento
    imagens_ruins_processadas.append(imagem_processada)

# Criar clipes de vídeo para imagens boas
clips_boas = [ImageClip(img).set_duration(1) for img in imagens_boas_processadas]

# Criar clipes de vídeo para imagens ruins
clips_ruins = [ImageClip(img).set_duration(1) for img in imagens_ruins_processadas]



clips = [ImageClip(img).set_duration(1) for img in ["1.jpeg","2.jpeg","3.jpeg"]]

videos= [CompositeVideoClip([
    clip.fx(transfx.slide_out, duration=0.4, side="left")])
    for clip in clips
]
video = concatenate_videoclips(videos, method="compose")
video.write_videofile("output.mp4",
    codec="libx264", audio_codec="aac",
    preset="ultrafast", fps=24,
    ffmpeg_params=[
        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
        "-pix_fmt", "yuv420p"
    ]
)


# Criar o vídeo
video = mp.ImageSequenceClip(frames, fps=fps)
video = video.set_duration(duracao_video)

# Salvar o vídeo
video.write_videofile('esteira_simulacao.mp4')