from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import os


def fn(x):
    '''
    we want either black or white pixels
    '''
    thresh = 200
    return 255 if x > thresh else 0


img = Image.open('download', 'r')
img = img.convert('L').point(fn, mode='1')
img.save('map.png')
data = np.asarray(img)
os.remove('download')

# img.show()
# plt.imshow(data, interpolation='nearest')
# plt.show()


# True = white pixels
# False = black pixels

height, width = len(data), len(data[0])
print('Map size: ', width, ' x ', height, '\n')

# we need to cut top and left part of the picture
cut_left = 0
done = False
for i in range(width):
    if done:
        break
    for j in range(40):
        if data[height // 2 + j][i] == True:
            cut_left = i
            done = True
            break

cut_top = 0
done = False
for i in range(height):
    if done:
        break
    for j in range(40):
        if data[i][width // 2 + j] == True:
            cut_top = i
            done = True
            break

# inserting pixels into ans list
ans = []
for i in range(cut_top, height):
    row = []

    for j in range(cut_left, width):
        pixel = data[i][j]
        row.append('#' if pixel else ' ')

    ans.append(row)

# save sokoban map to file to check if its good
with open('out.txt', 'w+') as o:
    for x in ans:
        o.write(''.join(str(w) for w in x))
        o.write('\n')


block_size = 64
SOKOBAN_MAP = []


def map_square(x, y):
    '''
    count numbers of white and black pixels in 64 x 64 block square
    @returns:
        64 x 64 block mapped to a char
    '''
    black_no, white_no = 0, 0
    for i in range(block_size):
        for j in range(block_size):
            if ans[x + i][y + j] == '#':
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


# iterate through all 64 x 64 blocks
N, M = len(ans), len(ans[0])
for i in range(0, N, block_size):
    row = []
    for j in range(0, M, block_size):
        if i + block_size < N and j + block_size < M:
            pixels = map_square(i, j)
            row.append(pixels)

    SOKOBAN_MAP.append(row)


for row in SOKOBAN_MAP:
    print(*row)

# let's save out map to txt
with open('map.txt', 'w') as f:
    for row in SOKOBAN_MAP:
        f.write(''.join(row) + '\n')


# Lets run our BFS
import BFS

# Now we need to make our keyboard print the answer
import write
