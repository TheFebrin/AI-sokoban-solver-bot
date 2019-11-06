from collections import deque
import sys, os
this_dir = sys.path[0]


MAP = []
ALL_STATES = set()
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]
N, M = 0, 0
sokoban_pos = (0, 0)
chests, goals, good_chests = [], [], {}

def print_info():

    print('C - chest')
    print('G - goal')
    print('P - player')
    print('# - wall \n')

    print('\n <Beginning state> \n')
    for m in MAP:
        print(*m)

    print('\n <Looking for solution> \n')

def read_map():
    img_path = os.path.join(this_dir, '../bin/text/map.txt')
    with open(img_path) as f:
        for line in f:
            if len(line) > 1:
                MAP.append(list(line.strip()))

def init_data():
    # extract all positions
    # P - player's position
    # C - chest's position
    # G - goal's position
    # * - chest laying on goal

    global sokoban_pos, chests, goals, good_chests
    for i in range(N):
        for j in range(M):
            if MAP[i][j] == 'P':
                sokoban_pos = (i, j)
            if MAP[i][j] == 'C':
                chests.append((i, j))
            if MAP[i][j] == 'G':
                good_chests[(i, j)] = False
                goals.append((i, j))
            if MAP[i][j] == '*':
                good_chests[(i, j)] = True
                chests.append((i, j))
                goals.append((i, j))

            if MAP[i][j] != '#':
                MAP[i][j] = '.'


def direction(x):
    return ['right', 'left', 'down', 'up'][x]


def hash_state(x, y, state):
    chests = tuple(state[1])
    return ((x, y), chests)


def hash_all(state):
    pos = state[0]
    chests = tuple(state[1])
    good = tuple(state[2].items())
    return (pos, chests, good)


def is_there_a_chest(x, y, chests):
    for c in chests:
        if c == (x, y):
            return True
    return False


def blocked_chest(x, y):
    cnt = 0
    for i in range(4):
        if MAP[x + dx[i]][y + dy[i]] == '#':
            cnt += 1

    return cnt >= 3


def good_move(x, y, state, direction):
    if not(0 <= x < N) or not(0 <= y < M) or MAP[x][y] == '#':
        return False

    hs = hash_state(x, y, state)
    chests = state[1]

    for chest in chests:
        if MAP[chest[0]][chest[1]] == '#' or blocked_chest(chest[0], chest[1]):
            return False

    if is_there_a_chest(x, y, chests):
        if direction == 'down' and x + 1 < N and (is_there_a_chest(x + 1, y, chests) or MAP[x + 1][y] == '#'):
            return False

        if direction == 'up' and x - 1 >= 0 and (is_there_a_chest(x - 1, y, chests) or MAP[x - 1][y] == '#'):
            return False

        if direction == 'right' and y + 1 < M and (is_there_a_chest(x, y + 1, chests) or MAP[x][y + 1] == '#'):
            return False

        if direction == 'left' and y - 1 >= 0 and (is_there_a_chest(x, y - 1, chests) or MAP[x][y - 1] == '#'):
            return False
    else:
        if hs in ALL_STATES:
            return False

    ALL_STATES.add(hs)
    return True


def move_chest(x, y, direction, chests, good_chests):
    vector = (dx[direction], dy[direction])

    for i in range(len(chests)):
        c_x = chests[i][0]
        c_y = chests[i][1]
        if c_x == x and c_y == y:
            if chests[i] in goals:
                good_chests[chests[i]] = False
            chests[i] = (c_x + vector[0], c_y + vector[1])
            if chests[i] in goals:
                good_chests[chests[i]] = True


def win(good_chests):
    for c in good_chests.items():
        if not c[1]:
            return False
    return True


def print_map(state):
    # system('clear')
    MAP2 = [[] for _ in range(N)]
    for i in range(N):
        MAP2[i] = MAP[i].copy()

    s_pos = state[0]
    chests = state[1]
    MAP2[s_pos[0]][s_pos[1]] = 'P'
    for c in chests:
        MAP2[c[0]][c[1]] = 'C'

    for m in MAP2:
        print(*m)

    print()


def print_answer(state):
    print('Number of steps needed: ', len(state[3]))
    print()
    steps = [direction(i) for i in state[3]]
    # steps = ', '.join(steps)
    # print(steps.title(), end='\n\n')
    print(steps)
    with open('text/steps.txt', 'w') as f:
        for step in steps:
            f.write(step + ' ')


def run_bfs():
    global N, M, sokoban_pos, chests, good_chests

    read_map()
    print_info()
    N, M = len(MAP), len(MAP[0])
    init_data()

    Q = deque()
    state = (sokoban_pos, chests, good_chests, [])
    Q.append(state)
    ALL_STATES.add(hash_state(sokoban_pos[0], sokoban_pos[1], state))

    cnt = 0
    while len(Q) > 0:
        act_state = Q.popleft()
        cnt += 1
        if cnt % 10000 == 0:
            print('States visited: ', cnt)
        # print(act_state)
        # print_map(act_state)

        if win(act_state[2]):
            print('\n <SOLUTION FOUND!> \n')
            print_map(act_state)
            print_answer(act_state)
            break

        s_pos = act_state[0]
        for i in range(4):
            new_x = s_pos[0] + dx[i]
            new_y = s_pos[1] + dy[i]
            chests, good_chests = act_state[1].copy(), act_state[2].copy()
            moves = act_state[3].copy()
            # print(s_pos, ' ---> ', (new_x, new_y), direction(i))

            if good_move(new_x, new_y, act_state, direction(i)):
                if is_there_a_chest(new_x, new_y, act_state[1]):
                    move_chest(new_x, new_y, i, chests, good_chests)

                moves.append(i)
                new_state = ((new_x, new_y), chests, good_chests, moves)
                Q.append(new_state)
