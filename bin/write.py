import keyboard
import time

steps = []
with open('search_algorithms/steps.txt') as f:
    s = f.readlines()
    for step in s[0].split():
        steps.append(step)

print('\nPress ENTER to start!')
keyboard.wait('enter')

# Click to make a move MODE
for move in steps:
    print(move)
    if move == 'up':
        keyboard.press('up')

    if move == 'down':
        keyboard.press('down')

    if move == 'left':
        keyboard.press('left')

    if move == 'right':
        keyboard.press('right')

    print('\nPress ENTER to make next move!')
    keyboard.wait('enter')

'''
# Auto moves mode

for move in steps:
    print(move)
    if move == 'up':
        keyboard.press('up')

    if move == 'down':
        keyboard.press('down')

    if move == 'left':
        keyboard.press('left')

    if move == 'right':
        keyboard.press('right')

    time.sleep(0.28)
'''
