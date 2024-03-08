
from predict import predict_image
from utils import measure_similarity, replace_chars
import easyocr

tests = [
    "images_to_test/img1.png",
    "images_to_test/img2.png",
    "images_to_test/img3.png",
    "images_to_test/img4.png",
    "images_to_test/img5.png",
    "images_to_test/img6.png",
]
expect_results = [
    "Legível", 
    "Legível", 
    "Legível", 
    "Ilegível", 
    "Ilegível", 
    "Ilegível"
]

reader = easyocr.Reader(['en'])
results = []

for image_path in tests:
    predict, score = predict_image(reader, image_path)
    score_med = sum(score) / len(score)
    predict = replace_chars(predict)    
    similarity_format = measure_similarity(predict)

    print("Previsão:", predict)
    print("Media de Score:", score_med)
    print("Média de Simularidade com formato:", similarity_format)
    
    if(score_med < 0.5 and similarity_format < 0.5):
        print("Ilegível")
        results.append("Ilegível")
    elif((score_med > 0.5) or (similarity_format > 0.6)):
        print("Legível")
        results.append("Legível")

matchs = sum(1 for x, y in zip(expect_results, results) if x == y)
print(matchs, "/", len(expect_results))
matchs_perc = (matchs / len(expect_results)) * 100

print("Resultados:", results)
print("Porcentagem de acertos:", matchs_perc, "%")
