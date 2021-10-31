import numpy as np
import cv2
import random
import sys

SIZE1 = 1080
SIZE2 = 1920

X_MIN = -6
X_MAX = 6
X_RANGE = X_MAX - X_MIN
Y_MIN = -8
Y_MAX = Y_MIN + X_RANGE * SIZE2 / SIZE1
Y_RANGE = Y_MAX - Y_MIN

ITER_NUM = 100


def display_progress(x, total):
    sys.stdout.write('\r    %4.2f'%(x / total))
    sys.stdout.flush()


def f_img(points):
    points_num = len(points)

    func_y = np.poly1d(points, True)
    func_dy = func_y.deriv(1)
    
    IMG = np.zeros([SIZE1, SIZE2])
    VALUE = np.zeros([SIZE1, SIZE2], dtype=complex)

    print('\n   phase 1/3')
    for x_i in range(SIZE1):
        display_progress(x_i, SIZE1)
        for y_i in range(SIZE2):
            point_x = x_i / SIZE1 * X_RANGE + X_MIN
            point_y = y_i / SIZE2 * Y_RANGE + Y_MIN
            VALUE[x_i, y_i] = complex(point_x, point_y)

    print('\n   phase 2/3')
    for it_i in range(ITER_NUM):
        display_progress(it_i, ITER_NUM)
        VALUE = VALUE - func_y(VALUE) / func_dy(VALUE)


    print('\n   phase 3/3')
    for x_i in range(SIZE1):
        display_progress(x_i, SIZE1)
        for y_i in range(SIZE2):
            temp_v = VALUE[x_i, y_i]
            dist = np.zeros([points_num])
            for p_i in range(points_num):
                dist[p_i] = abs(temp_v - points[p_i])
            color_i = np.argmin(dist)
            IMG[x_i, y_i] = color_i / points_num * 0.5

    return IMG

IMAGE_LIST = []
for img_i in range(10):
    print('\n\nIMG ', img_i)
    points = []
    for p_i in range(10):
        a = (random.random() - 0.5) * 2 * X_RANGE
        b = (random.random() - 0.5) * 2 * Y_RANGE
        points.append(complex(a, b))
    IMAGE_LIST.append(f_img(points))

IMG_AVE = np.zeros_like(IMAGE_LIST[0])
for img_i in range(len(IMAGE_LIST)):
    IMG_AVE += IMAGE_LIST[img_i] * (1 / len(IMAGE_LIST))

cv2.imwrite('img.png', IMG_AVE*255)

print('FINISHED')
