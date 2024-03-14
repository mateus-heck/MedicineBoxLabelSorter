
from predict import predict_image
from utils import measure_similarity, replace_chars
import easyocr
import time

# tests = [
#     "images_to_test/img1.png",
#     "images_to_test/img2.png",
#     "images_to_test/img3.png",
#     "images_to_test/img4.png",
#     "images_to_test/img5.png",
#     "images_to_test/img6.png",
# ]
x = 255
tests = ["images_ger/result_" + str(indice) + ".png" for indice in range(x)]
# expect_results = [
#     "Legível", 
#     "Ilegível", 
#     "Legível", 
#     "Ilegível", 
#     "Ilegível", 
#     "Ilegível"
# ]
expect_results = ["Legível" for indice in range(x)]

print("Testes:", len(tests))
print("Esperado:", len(expect_results))
print(expect_results[0])
print(tests[0])

reader = easyocr.Reader(['en'], gpu=True)
results = []
inicio = time.time()
for image_path in tests:
    predict, score = predict_image(reader, image_path)
    score_med = sum(score) / len(score)
    predict = replace_chars(predict)    
    similarity_format = measure_similarity(predict)
    
    if(score_med > 0.5) or (similarity_format > 0.6):
        results.append("Legível")
    else:
        results.append("Ilegível")
fim = time.time()
print("Tempo de execução:", fim - inicio)
matchs = sum(1 for x, y in zip(expect_results, results) if x == y)
print(matchs, "/", len(expect_results))
matchs_perc = (matchs / len(expect_results)) * 100

print("Resultados:", results)
print("Porcentagem de acertos:", matchs_perc, "%")
