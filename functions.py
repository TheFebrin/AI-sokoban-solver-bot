from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import os

block_size = 64
SOKOBAN_MAP = []
raw_map, reduced_map = [], []
height, width = 0, 0

def fn(x):
    '''
    Convert image,
    Make black / white pixels
    '''
    thresh = 200
    return 255 if x > thresh else 0


def import_map_image():
    '''
    Import image reduced_map save it as B&W np array
    True = white pixels
    False = black pixels
    '''
    global raw_map, width, height
    img = Image.open('download', 'r')
    img = img.convert('L').point(fn, mode='1')
    img.save('map.png')
    raw_map = np.asarray(img)
    # os.remove('download')

    height, width = len(raw_map), len(raw_map[0])
    print('Map size: ', width, ' x ', height, '\n')
    # img.show()
    # plt.imshow(raw_map, interpolation='nearest')
    # plt.show()


def cut():
    '''
    Cut top and left part of the map
    '''
    cut_left = 0
    done = False
    for i in range(width):
        if done:
            break
        for j in range(40):
            if raw_map[height // 2 + j][i] == True:
                cut_left = i
                done = True
                break

    cut_top = 0
    done = False
    for i in range(height):
        if done:
            break
        for j in range(40):
            if raw_map[i][width // 2 + j] == True:
                cut_top = i
                done = True
                break

    # inserting pixels into reduced_map list
    global reduced_map
    for i in range(cut_top, height):
        row = []
        for j in range(cut_left, width):
            pixel = raw_map[i][j]
            row.append('#' if pixel else ' ')

        reduced_map.append(row)




def create_map():
    '''
    iterate through all blocks,
    '''
    N, M = len(reduced_map), len(reduced_map[0])
    for i in range(0, N, block_size):
        row = []
        for j in range(0, M, block_size):
            if i + block_size < N and j + block_size < M:
                pixels = map_squares(i, j)
                row.append(pixels)

        SOKOBAN_MAP.append(row)


def map_squares(x, y):
    '''
    count numbers of white and black pixels in one block square
    creates map readable for computer
    '''

    black_no, white_no = 0, 0
    for i in range(block_size):
        for j in range(block_size):
            if reduced_map[x + i][y + j] == '#':
                white_no += 1
            else:
                black_no += 1

    ratio = black_no - white_no
    # return ratio

    if 1700 <= ratio <= 1800:
        return '#'  # wall block

    if ratio >= 4001:
        return '#'  # empty field outside of the map

    if ratio <= -4000:
        return '.'  # empty block

    if -4001 <= ratio <= -3800:
        return 'G'  # goal

    if 3800 <= ratio <= 3850:
        return 'C'  # chest

    if 3858 <= ratio <= 4000:
        return '*'  # chest on goal

    if -1500 <= ratio <= -900:
        return 'P'  # Player


def save_map():
    '''
    Save sokoban map to file
    '''
    with open('map.txt', 'w') as f:
        for row in SOKOBAN_MAP:
            f.write(''.join(row) + '\n')

def get_raw_map():
    return raw_map

def get_reduced_map():
    return reduced_map
