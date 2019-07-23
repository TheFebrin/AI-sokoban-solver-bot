from functions import *
# import functions

def cut(data):
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
    global ans
    for i in range(cut_top, height):
        row = []
        for j in range(cut_left, width):
            pixel = data[i][j]
            row.append('#' if pixel else ' ')

        ans.append(row)


def map_squares(x, y):
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


def create_map(ans):
    '''
    iterate through all blocks,

    '''
    N, M = len(ans), len(ans[0])
    for i in range(0, N, block_size):
        row = []
        for j in range(0, M, block_size):
            if i + block_size < N and j + block_size < M:
                pixels = map_squares(i, j)
                row.append(pixels)

        SOKOBAN_MAP.append(row)


if __name__ == '__main__':
    import_image()
    height, width = get_map_size()
    print('Map size: ', width, ' x ', height, '\n')
    cut(get_data())
    save_map()
    create_map(get_ans())

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
