import numpy as np
import cv2
import random
import sys
import torch


DEVICE = torch.device('cuda:0')

SIZE1 = 1080
SIZE2 = 1920
SIZE1 = 2160
SIZE2 = 3840

X_MIN = -6
X_MAX = 6
X_RANGE = X_MAX - X_MIN
Y_MIN = -8
Y_MAX = Y_MIN + X_RANGE * SIZE2 / SIZE1
Y_RANGE = Y_MAX - Y_MIN

ITER_NUM = 200


def display_progress(x, total):
    sys.stdout.write('\r    %4.2f'%(x / total))
    sys.stdout.flush()


def f_img(points):
    points_num = len(points)

    func_y = np.poly1d(points, True)
    func_dy = func_y.deriv(1)
    
    VALUE = torch.zeros([SIZE1, SIZE2], dtype=torch.cfloat, device=DEVICE)

    print('\n   phase 1/3')
    VALUE[:, :].real = (X_MIN + torch.arange(SIZE1) * X_RANGE / SIZE1).expand([SIZE2, SIZE1]).permute([1, 0])
    display_progress(1, 2)
    VALUE[:, :].imag = (Y_MIN + torch.arange(SIZE2) * Y_RANGE / SIZE2).expand([SIZE1, SIZE2])
    display_progress(2, 2)
    # for x_i in range(SIZE1):
    #     display_progress(x_i, SIZE1)
    #     for y_i in range(SIZE2):
    #         point_x = x_i / SIZE1 * X_RANGE + X_MIN
    #         point_y = y_i / SIZE2 * Y_RANGE + Y_MIN
    #         VALUE[x_i, y_i] = complex(point_x, point_y)

    print('\n   phase 2/3')
    for it_i in range(ITER_NUM):
        display_progress(it_i+1, ITER_NUM)

        V_FY = torch.zeros_like(VALUE)
        for p_i in range(points_num+1):
            V_FY = V_FY + func_y[p_i] * (VALUE ** p_i)
        V_FDY = torch.zeros_like(VALUE)
        for p_i in range(points_num):
            V_FDY = V_FDY + func_dy[p_i] * (VALUE ** p_i)
        VALUE = VALUE - V_FY / V_FDY

    print('\n   phase 3/3')
    dist = torch.zeros([SIZE1, SIZE2, points_num])
    for p_i in range(points_num):
        display_progress(p_i+1, points_num)
        dist[:, :, p_i] = torch.abs(VALUE - points[p_i])
    color_i = torch.argmin(dist, axis=2).cpu().numpy()
    IMG = (color_i / points_num * 0.5)
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

print('\n\nFINISHED')
