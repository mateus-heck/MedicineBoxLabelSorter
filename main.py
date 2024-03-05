import cv2
import pytesseract
import easyocr
import matplotlib.pyplot as plt

image_path = r'img_tratada.png'
image = cv2.imread(image_path)
if image is None:
    raise ValueError("Invalid image file or path.")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0) #Mexer aqui
bw = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

kernel_size = (15, 1) 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
bw_closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
contours, _ = cv2.findContours(bw_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
filtered_contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3])>=3.0]
sorted_contours = sorted(filtered_contours, key=lambda contour: cv2.boundingRect(contour)[1])

reader = easyocr.Reader(['en'])
predict = []
padding=3
for contour in sorted_contours:
    x, y, w, h = cv2.boundingRect(contour)
    x, y, w, h = (x-padding, y-padding, w+padding, h+padding) 
    line_image = bw[y:y + h, x:x+w]
    plt.imshow(cv2.cvtColor(line_image, cv2.COLOR_BGR2RGB))
    plt.show()
    raw_predict = reader.readtext(line_image)
    if(len(raw_predict)>0):
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        predict.append(raw_predict[0][1])
    print("\nPredict: ", raw_predict)
    print("Score: ", raw_predict)

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
