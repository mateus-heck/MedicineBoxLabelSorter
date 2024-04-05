import cv2

def redimensionar_imagem(input_path):
    image = cv2.imread(input_path +".jpg")

    altura_atual, largura_atual = image.shape[:2]
    largura_atual = 500
    altura_atual = 180
    image = cv2.resize(image, (int(largura_atual), int(altura_atual)))
  
    cv2.imwrite("files/new_imgs_red/"+input_path+".png", image)

x = 36
tests = [str(indice+1) for indice in range(x)]

for test in tests:
  redimensionar_imagem(test)
