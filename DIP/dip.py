import cv2
import numpy as np

def remove_line(im):
    temp = im.copy()
    thresh = cv2.threshold(temp, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        cv2.drawContours(temp, [c], -1, (255,255,255), 3)
    return temp

def tophalf(image, gray):
    box = []
    with_no_line = remove_line(gray)
    # kernel = np.ones((3, 3), np.uint8)
    # with_no_line = cv2.erode(with_no_line, kernel, iterations=1)
    # with_no_line = cv2.dilate(with_no_line, kernel, iterations=1)
    thresh = cv2.adaptiveThreshold(with_no_line, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                    cv2.THRESH_BINARY, 3, 1)
    # cv2.imshow('thresh', thresh)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    box_counter = 0
    for cnt in contours:
        [x, y, w, h] = cv2.boundingRect(cnt)
        if cv2.contourArea(cnt) > 250 and cv2.contourArea(cnt) < 800:
            if w > 10 and w < 40 and h > 35 and h < 70 and y < 190:
                box.append([(x, y), (x+w, y+h)])
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv2.imshow('im', image)
def line4(image, gray):
    count = 0
    with_no_line = remove_line(gray)
    # with_no_line = cv2.fastNlMeansDenoising(with_no_line, None, 11, 7, 11)
    _, thresh = cv2.threshold(with_no_line, 70, 255, cv2.THRESH_BINARY)
    kernel = np.ones((2, 2), np.uint8)
    with_no_line = cv2.erode(thresh, kernel, iterations=1)
    thresh = cv2.adaptiveThreshold(with_no_line, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                    cv2.THRESH_BINARY, 5, 1)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 250 and cv2.contourArea(cnt) < 800:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if w > 10 and w < 40 and h > 35 and h < 70 and y > 195 and y < 270:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                count += 1
    cv2.imshow('im', image)
    print(count)
    cv2.imshow('thresh', thresh)
    cv2.imshow('res', with_no_line)

# def line4(image, gray):
#     count = 0
#     with_no_line = remove_line(gray)
#     # with_no_line = cv2.fastNlMeansDenoising(with_no_line, None, 3, 7, 11)
#     # kernel = np.ones((5, 5), np.uint8) / 25
#     # with_no_line = cv2.filter2D(with_no_line, -1, kernel)
#     with_no_line = cv2.GaussianBlur(with_no_line, (5, 5), 0)
#     # with_no_line = cv2.medianBlur(with_no_line, 5)
#     ret, thresh = cv2.threshold(with_no_line, 100, 255, cv2.THRESH_BINARY)
#     with_no_line = cv2.bitwise_or(with_no_line, thresh)
#     # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 1))
#     # with_no_line = cv2.dilate(with_no_line, kernel, iterations=1)
#     # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
#     # with_no_line = cv2.erode(with_no_line, kernel, iterations=1)
#     thresh = cv2.adaptiveThreshold(with_no_line, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
#                     cv2.THRESH_BINARY, 11, 1)
#     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     for cnt in contours:
#         if cv2.contourArea(cnt) > 250 and cv2.contourArea(cnt) < 800:
#             [x, y, w, h] = cv2.boundingRect(cnt)
#             if w > 10 and w < 40 and h > 35 and h < 70 and y > 205 and y < 260:
#                 cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
#                 count += 1
#     cv2.imshow('im', image)
#     print(count)
#     cv2.imshow('thresh', thresh)
#     cv2.imshow('res', with_no_line)

def line5(image, gray):
    with_no_line = remove_line(gray)
    thresh = cv2.adaptiveThreshold(with_no_line, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                    cv2.THRESH_BINARY, 5, 1)
    count = 0
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 250 and cv2.contourArea(cnt) < 800:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if w > 10 and w < 40 and h > 35 and h < 70 and y > 265 and y < 325 and x < 165:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                count += 1
    blur = cv2.GaussianBlur(with_no_line, (3, 3), 0) 
    # blur = cv2.medianBlur(with_no_line, 3)   
    _, thresh = cv2.threshold(blur, 45, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 250 and cv2.contourArea(cnt) < 800:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if w > 10 and w < 40 and h > 35 and h < 70 and y > 265 and y < 325 and x > 165:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                count += 1
    cv2.imshow('box', image)
    cv2.imshow('thresh2', thresh)
    print(count)

def line6(image, gray):
    with_no_line = remove_line(gray)
    count = 0
    neg = 255 - with_no_line
    thresh = cv2.threshold(neg, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for cnt in contours:
        [x, y, w, h] = cv2.boundingRect(cnt)
        if w > 10 and w < 40 and h > 35 and h < 70 and y > 325 and x < 185:
            cv2.rectangle(image, (x,y), (x+w,y+h), (0, 0, 255), 2)
            count += 1
    cv2.imshow('image', image)
    
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(2, 2))
    # with_no_line = cv2.erode(with_no_line, kernel, iterations=1)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16, 16))
    with_no_line = clahe.apply(with_no_line)

    # kernel = np.ones((5, 5), np.uint8) / 25
    # with_no_line = cv2.filter2D(with_no_line, -1, kernel)
    # with_no_line = cv2.GaussianBlur(with_no_line, (7, 7), 0)
    with_no_line = cv2.medianBlur(with_no_line, 5)
    _, thresh = cv2.threshold(with_no_line, 70, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 250 and cv2.contourArea(cnt) < 800:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if w > 10 and w < 40 and h > 35 and h < 70 and y > 325 and x > 180:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv2.imshow('t', image)
    cv2.imshow('thresh', thresh)

im = cv2.imread('image.png')
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
tophalf(im, gray)
line4(im, gray)
line5(im, gray)
line6(im, gray)
cv2.waitKey()