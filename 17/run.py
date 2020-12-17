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


strips = lambda l: list(map(str.strip, l))
ints = lambda l: list(map(int, l))
commas = lambda s: s.split(",")
comma_ints = lambda s: ints(strips(s.split(",")))

print(commas("1,2,3,4,5"))

L, I, D, S = list, int, dict, set
P, E, R, M = print, enumerate, range, map

############### end of boilerplate #############################################

import numpy as np


def line_transform(line):
    # split = [line.split() for line in lines]
    # return int(line)
    return line


lines = [line_transform(line) for line in lines]  # apply line_transform to each line

DIM = 50
# world = [[["."] * DIM] * DIM] * DIM
world = [
    [[[[False] for w in range(DIM)] for k in range(DIM)] for j in range(DIM)]
    for i in range(DIM)
]
world = np.array(world, dtype=bool)
woffset = DIM // 2
zoffset = DIM // 2
yoffset = DIM // 2
xoffset = DIM // 2
for line in lines:
    # put in middle
    for idx, c in E(line):
        print(zoffset, yoffset, xoffset, idx, c)
        world[woffset][zoffset][yoffset][xoffset + idx] = c
    yoffset += 1
# print(world)

slice_dims = [[0, 0], [0, 0], [0, 0], [0, 0]]


def neighbors(world_, x, y, z, w):
    offs = (-1, 0, 1)
    adj = 0
    for dw in offs:
        for dz in offs:
            for dy in offs:
                for dx in offs:
                    if dx == dy == dz == dw == 0:
                        continue
                    xx = x + dx
                    yy = y + dy
                    zz = z + dz
                    ww = w + dw
                    if any([yy < 0, xx < 0, zz < 0, ww < 0]):
                        continue
                    if any([yy >= DIM, xx >= DIM, zz >= DIM, ww >= DIM]):
                        continue
                    if world_[ww][zz][yy][xx] == True:
                        adj += 1
    return adj


def round(_seats):
    nu_seats = deepcopy(_seats)
    for w in range(DIM):
        for z in range(DIM):
            for y in range(DIM):
                for x in range(DIM):
                    adj = neighbors(_seats, x, y, z, w)
                    cur = _seats[w][z][y][x]
                    if cur == True:
                        if adj not in (2, 3):
                            nu_seats[w][z][y][x] = False
                    if cur == False and adj == 3:
                        nu_seats[w][z][y][x] = True
    return nu_seats


def active(seats):
    tot = 0
    for w in range(DIM):
        for z in range(DIM):
            for y in range(DIM):
                for x in range(DIM):
                    if seats[w][z][y][x] == True:
                        tot += 1
    return tot


print(active(world))
# exit()
for i in range(6):
    # print(world)
    acc = active(world)
    print(acc)
    world = round(world)

ans(acc)

# not 307
# part 1:  346?
