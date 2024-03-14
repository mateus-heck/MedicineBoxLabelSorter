from PIL import Image

def redimensionar_imagem(input_path, largura, altura):
    # Abrir a imagem
    imagem = Image.open("images_ger/"+ input_path)
    
    # Redimensionar a imagem
    imagem_redimensionada = imagem.resize((largura, altura))
    
    # Salvar a imagem redimensionada
    imagem_redimensionada.save("images_re/"+input_path)

x = 255
# Exemplo de uso
tests = ["result_" + str(indice) + ".png" for indice in range(x)]
largura = 250
altura = 150

for test in tests:
  redimensionar_imagem(test, largura, altura)
