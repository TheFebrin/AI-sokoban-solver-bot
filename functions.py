from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import os

block_size = 64
SOKOBAN_MAP = []
data = []
height, width = 0, 0
ans = []

def fn(x):
    '''
    Used to convert image,
    makes either black or white pixels
    '''
    thresh = 200
    return 255 if x > thresh else 0


def import_image():
    '''
    True = white pixels
    False = black pixels
    '''
    global data, width, height
    img = Image.open('download', 'r')
    img = img.convert('L').point(fn, mode='1')
    img.save('map.png')
    data = np.asarray(img)
    # os.remove('download')

    height, width = len(data), len(data[0])
    # img.show()
    # plt.imshow(data, interpolation='nearest')
    # plt.show()


def save_map():
    '''
    save sokoban map to file,
    so BFS can use it
    '''
    global ans
    with open('out.txt', 'w+') as o:
        for x in ans:
            o.write(''.join(str(w) for w in x))
            o.write('\n')

def get_map_size():
    return height, width


def get_data():
    return data

def get_ans():
    return ans
