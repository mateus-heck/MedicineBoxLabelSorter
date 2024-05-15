import numpy as np 
import cv2 as cv

class LineIntersection:
    """
    This class represents line intersection logic. It takes four points, 
    calculates the equations of the first two lines and the last two lines, 
    and finds their intersection point.
    """

    def __init__(self, point1, point2, point3, point4):
        """
        Initializes the class with four points.

        Args:
            point1: A tuple representing the first point (x1, y1).
            point2: A tuple representing the second point (x2, y2).
            point3: A tuple representing the third point (x3, y3).
            point4: A tuple representing the fourth point (x4, y4).
        """

        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.point4 = point4

    def get_line_equation(self, point1, point2):
        """
        Calculates the equation of the line (ax + by + c = 0) 
        given two points.

        Args:
            point1: A tuple representing the first point (x1, y1).
            point2: A tuple representing the second point (x2, y2).

        Returns:
            A tuple containing the slope (m) and y-intercept (c) of the line.
        """

        x1, y1 = point1
        x2, y2 = point2
        
        # Handle special cases (vertical and horizontal lines)
        if x1 == x2:
            return 0, 1,  x1  # Line is vertical, equation: x = constant
        elif y1 == y2:
            return 0, 1,  y1  # Line is horizontal, equation: y = constant

        # Calculate slope (m)
        m = (y2 - y1) / (x2 - x1)

        # Calculate y-intercept (c)
        c = y1 - (m * x1)
        return m, 1, c

    def find_intersection(self):
        """
        Finds the intersection point between the first two lines and 
        the last two lines.

        Returns:
            A tuple containing the x and y coordinates of the intersection point, 
            or None if the lines are parallel or coincident.
        """
        # Get line equations for first two lines and last two lines
        line1_coeffs = self.get_line_equation(self.point1, self.point2)
        line2_coeffs = self.get_line_equation(self.point3, self.point4)
        print(line1_coeffs)
        print(line2_coeffs)
        # Check if any line is invalid (vertical or horizontal)
        if line1_coeffs is None or line2_coeffs is None:
            return None
        
        # Define the find_intersection function within the class (alternative)
        def find_intersection(line1_coeffs, line2_coeffs):
            """
            This function finds the intersection point of two lines given their 
            coefficients in the form ax + by + c = 0.

            Args:
                line1_coeffs: A tuple containing coefficients (a, b, c) for line 1.
                line2_coeffs: A tuple containing coefficients (a, b, c) for line 2.

            Returns:
                A tuple containing the x and y coordinates of the intersection point, 
                or None if the lines are parallel or coincident.
            """
            
            a1, b1, c1 = line1_coeffs
            a2, b2, c2 = line2_coeffs

            # Calculate determinants
            D = a1 * b2 - a2 * b1
            D_x = c1 * b2 - c2 * b1
            D_y = a1 * c2 - a2 * c1

            # Check for parallel or coincident lines
            if D == 0:
                return None

            # Calculate intersection point coordinates
            x = D_x / D
            y = D_y / D
            print(x, y)
            return x, y

        # Call the defined function within the class
        intersection_point = find_intersection(line1_coeffs, line2_coeffs)
        #give the abs value of the intersection point
        intersection_point = [int(abs(intersection_point[0])), int(abs(intersection_point[1]))]
        return intersection_point

def get_contours(img, weight):
    dilated_image = cv.dilate(img, np.ones((3, 3), np.uint8), iterations=weight)
    if weight == 20:
        dilated_image = cv.bitwise_not(dilated_image)    
    ret,thresh = cv.threshold(dilated_image,127,255,50)
    contours,hierarchy = cv.findContours(thresh, 1, 2)
    aux = img.copy()
    # cv.drawContours(aux, contours, -1, (255, 255, 255), 2)
    # cv.imshow("Contours", aux)
    # cv.waitKey(0)
    if weight == 20:
        multiple_contours = []    
        for cnt in contours:
            multiple_contours += [cv.boundingRect(cnt)]
        return multiple_contours
    if len(contours[0]) > 20:
        for cnt in contours:
            approx = cv.approxPolyDP(cnt, 0.02*cv.arcLength(cnt, True), True)
            cv.minAreaRect(approx)
            # cv.drawContours(img, [approx], 0, (255, 255, 255), 3)
            # cv.imshow("Approx", img)
            # cv.waitKey(0)
        aux = approx.tolist()
        aux.sort(key=lambda x: x[0][-2], reverse=True)
        r1 = aux[0]
        r2 = aux[1]
        l1 = aux[-1]
        l2 = aux[-2]
        if l1[0][0] + l1[0][1] > l2[0][0] + l2[0][1]:
            l1, l2 = l2, l1
        if r1[0][1] > r2[0][1]:
            r1, r2 = r2, r1
        #define the rotation point of the second line
        if aux[-3][0][1] > aux[-4][0][1]:
            mid = aux[-3]
        else:
            mid = aux[-4]
        point1 = (l2[0][0], l2[0][1])
        point2 = (mid[0][0], mid[0][1])
        point3 = (r1[0][0], r1[0][1])
        point4 = (r2[0][0], r2[0][1])
        # print(point1, point2, point3, point4)              
        # cv.putText(img, f"{point1}", point1, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # cv.putText(img, f"{point2}", point2, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # cv.putText(img, f"{point3}", point3, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # cv.putText(img, f"{point4}", point4, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # cv.imshow("Approx", img)
        # cv.waitKey(0)

        line_intersection = LineIntersection(point1, point2, point3, point4)
        intersection_point = line_intersection.find_intersection()
        # # # print(rotation_2)
        # # # print(dif)
        # cv.circle(img, (r1[0][0], r1[0][1]), 5, (255, 255, 255), -1)
        # cv.circle(img, (l1[0][0], l1[0][1]), 5, (255, 255, 255), -1)
        # cv.putText(img, f"{l1}", (l1[0][0], l1[0][1]), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # cv.circle(img, (l2[0][0], l2[0][1]), 5, (255, 255, 255), -1)
        # cv.circle(img, (r2[0][0], r2[0][1]), 5, (255, 255, 255), -1)
        # # cv.circle(img, mid[0], 5, (255, 255, 255), -1)
        cv.circle(img, (intersection_point[0], intersection_point[1]), 5, (255, 255, 255), -1)
        # # # cv.putText(img, f'{rotation_2}', rotation_2, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # cv.imshow("Approx", img)
        cv.waitKey(0)
        point1 = [int(abs(point1[0])), int(abs(point1[1]))]
        point2 = [int(abs(point2[0])), int(abs(point2[1]))]
        point3 = [int(abs(point3[0])), int(abs(point3[1]))]
        return np.array([l1,[point1], [point3], [intersection_point]])


image_path = "v4/assets/real_imgs/img3.png"

img = cv.imread(image_path)
#extend the image 50 pixels each side
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = cv.inRange(img, 0, 150)
altura = img.shape[0]
#make 50x50 border gray
img = cv.copyMakeBorder(img, 50, 50, 50, 50, cv.BORDER_CONSTANT, value=0)
#invert black and white
# img = cv.bitwise_not(img)
# cv.imshow("Original Image", img)
# cv.waitKey(0)


response = get_contours(img, 50)
t_border = np.array(response)
# print(t_border)
x, y, w, h = cv.boundingRect(t_border)
# cv.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 3)
# cv.imshow("Bounding Box", img)
# cv.waitKey(0)
pts1 = np.float32([t_border[0],
                    t_border[1],
                    t_border[2],
                    t_border[3]])
if t_border[0][0][1] > 100:
    pts2 = np.float32([[[x, y+h]], [t_border[1][0]], [t_border[2][0]], [[x+w, y+h]]])
else:
    pts2 = np.float32([[x, y], t_border[1][0], t_border[2][0], [x+w, y+h]])
matrix = cv.getPerspectiveTransform(pts1, pts2)
img_edited = cv.warpPerspective(img, matrix, img.shape[::-1])
# cv.imshow("Pesrpective", img_edited)
cv.waitKey(0)
# crop where the rectangle is drawn

img = img_edited[y:y+h, x:x+w]
cv.imshow("Pesrpective", img)
cv.waitKey(0)
text_height = ((h-100)//3)
print(text_height)
img_1 = img[50:text_height+50, 0:w]
# img_1 = img[0:text_height, 0:text_height]
img_2 = img[text_height+50 : text_height*2 +50 , 0:x+w]
img_3 = img[text_height *2 +50 :text_height *3 + 50 , 0:x+w]
# cv.imshow("img_1", img_1)
# cv.imshow("img_2", img_2)
# cv.imshow("img_3", img_3)
# cv.waitKey(0)

img_1 = cv.copyMakeBorder(img_1, 50, 50, 0, 0, cv.BORDER_CONSTANT, value=0)
img_2 = cv.copyMakeBorder(img_2, 50, 50, 0, 0, cv.BORDER_CONSTANT, value=0)
img_3 = cv.copyMakeBorder(img_3, 50, 50, 0, 0, cv.BORDER_CONSTANT, value=0)
cv.imshow("img_1", img_1)
cv.imshow("img_2", img_2)
cv.imshow("img_3", img_3)
cv.waitKey(0)

# rec_1 = get_contours(img_1, 20)
# print(rec_1)
# print(img_1.shape)
# fab = img_1[rec_1[1][1]:rec_1[1][1] + rec_1[1][3], rec_1[1][0]+20:rec_1[1][0] + rec_1[1][2]-20]
# hour = img_1[rec_1[0][1]:rec_1[0][1] + rec_1[0][3], rec_1[0][0]+20:rec_1[0][0] + rec_1[0][2]-20]
# # cv.imshow("total 1", hour)
# # cv.imshow("total 2", fab)
# rec_2 = get_contours(img_2, 20)
# val = img_2[rec_2[0][1]:rec_2[0][1] + rec_2[0][3], rec_2[0][0]+20:rec_2[0][0] + rec_2[0][2]-20]
# # cv.imshow("total 3", val)
# rec_3 = get_contours(img_3, 20)
# lote = img_3[rec_3[0][1]:rec_3[0][1] + rec_3[0][3], rec_3[0][0]:rec_3[0][0] + rec_3[0][2]]
# cv.imshow("total 4", lote)
# cv.waitKey(0)

# imgs = [fab, hour, val, lote]
# for img in imgs:
#     cv.imshow("teste", img)
#     cv.waitKey(0)
# x_start = 0
# y_start = 0

# def get_digit(img, digits):
#     x_start = 0
#     square_size = img.shape[1]//digits
#     for i in range(digits):
#         x_end = x_start + square_size
#         y_end = img.shape[0]
#         # cv.rectangle(img, (x_start, y_start), (x_end, y_end), (0, 255, 0))
#         croped = img[y_start:y_end, x_start:x_end]
#         x_start += square_size
#         cv.imshow("teste", croped)
#         cv.waitKey(0)

# get_digit(fab, 6)
# get_digit(hour, 5)
# get_digit(val, 6)
# get_digit(lote, 7)

