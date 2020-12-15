############### boilerplate ####################################################
import os
from itertools import chain, combinations
from copy import deepcopy

# change to dir of script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    with open("input.txt") as f:
        data = f.read()  # entire file as string
        lines = data.splitlines()
except:
    print("no input.txt")
    data, lines = "", []

line_groups = data.split("\n\n")  # lines split by double newlines
print(lines)
print(len(lines), "lines in input.txt")


def coords(arr2d):
    # return [(x0,y0), (x1, y0), ...]
    coords = []
    for y in range(len(arr2d)):
        for x in range(len(arr2d[0])):
            coords.append((x, y))
    return coords


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def ans(answer):
    # store answer to clipboard
    print(answer, "| in clipboard")
    os.system(f'echo "{answer}"| xclip -selection clipboard -in')


L, I, D, S = list, int, dict, set
P, E, R, M = print, enumerate, range, map

############### end of boilerplate #############################################


def line_transform(line):
    # split = [line.split() for line in lines]
    # return int(line)
    return line.split(",")


lines = [line_transform(line) for line in lines]  # apply line_transform to each line

turn = 0
before = dict()
before2 = dict()
for num in data.split(","):
    num = int(num)
    before[num] = turn
    last = num
    turn += 1

last_novel = True
while True:
    if last_novel:
        to_speak = 0
    else:
        to_speak = before[last] - before2[last]
    last_novel = to_speak not in before.keys()
    before2[to_speak] = before.get(to_speak, None)
    before[to_speak] = turn
    last = to_speak
    turn += 1

    if turn == 2020:
        ans(to_speak)  # 1325
        # break

    if turn == 30000000:
        ans(to_speak)  # 59006
        break

    if turn % 10 ** 6 == 0:
        print(turn)
