import sys
import time
from PIL import Image
from multiprocessing import *
import numpy as np


class Profiler:
    def __init__(self):
        self._startTime = time.time()

    def print(self):
        print("Time: {:.3f} sec".format(time.time() - self._startTime))


core = {
    0: np.array([[[0.111111111], [0.111111111], [0.111111111]],
                 [[0.111111111], [0.111111111], [0.111111111]],
                 [[0.111111111], [0.111111111], [0.111111111]]]),

    1: np.array([[[1], [0], [-1]],
                 [[1], [0], [-1]],
                 [[1], [0], [-1]]]),

    3: np.array([[[-1.2], [0], [1.2]],
                 [[2], [0], [-2]],
                 [[-1.2], [0], [1.2]]]),

    4: np.array([[[-1.2], [1.8], [-1.2]],
                 [[0], [0], [0]],
                 [[1.2], [-1.8], [1.2]]]),

    5: np.array([[[0], [-1], [0]],
                 [[-1], [5], [-1]],
                 [[0], [-1], [0]]]),

    6: np.array([[[0], [-1], [0]],
                 [[-1], [4], [-1]],
                 [[0], [-1], [0]]])
}


def image_transform(image, transform):
    img_main = Image.open(image)

    width = img_main.size[0]
    height = img_main.size[1]

    pix = np.array(img_main)
    out = np.zeros((height, width, 3), dtype=np.uint8)
    print("height =", height, "\nwidth =", width)

    #   TODO подкорректировать позже
    if pix.shape[2] == 4:
        background = Image.new("RGB", img_main.size, (255, 255, 255))
        background.paste(img_main, mask=img_main.split()[3])
        pix = np.array(background)

    _core = core[transform]

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            pixel = (pix[i - 1:i + 2, j - 1:j + 2] * _core).sum(axis=1).sum(axis=0)

            for c in range(len(pixel)):
                if pixel[c] > 255:
                    pixel[c] = 255
                elif pixel[c] < 0:
                    pixel[c] = 0

            out[i, j] = pixel
            #   out[i, j] = np.select([pixel < 0, pixel > 255], [0, 255], default=pixel)

    return Image.fromarray(out)


# Проверим, что программа запущена с консоли
if __name__ == "__main__":
    # путь к картинке нам потребуется в любом случае
    if len(sys.argv) < 2:
        print("System's arguments are not enough!")
        print("[-image_path] [-mode]{optional}")
        exit(1)

    image_path = sys.argv[1]  # путь к картинке
    if len(sys.argv) < 3:
        # mode -- вариант преобразования
        mode = -1
        menu = "\nblur - 0", "hard borders - 1", \
               "ghost borders - 4", "sharpness - 5", "smart borders - 6"
        while mode not in core:
            print(*menu, sep="\n")
            mode = int(input("Enter your command: "))
    else:
        mode = int(sys.argv[2])

    p = Profiler()
    new_image = image_transform(image_path, mode)
    p.print()
    new_image.save("new_file_mode" + str(mode) + ".png")
