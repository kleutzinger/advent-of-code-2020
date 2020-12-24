############### boilerplate ####################################################
import os
import sys
import shutil
from itertools import chain, combinations
from copy import deepcopy

# change to dir of script
os.chdir(os.path.dirname(os.path.abspath(__file__)))
input_file = "input.txt"
if "s" in sys.argv:
    input_file = "input_small.txt"
try:
    with open(input_file) as f:
        data = f.read()  # entire file as string
        lines = data.splitlines()
except:
    print("no " + input_file)
    data, lines = "", []

line_groups = data.split("\n\n")  # lines split by double newlines
# line_groups = [l.strip() for l in line_groups]  # remove trailing newlines
# print(lines)
print(f"{len(lines)} lines in {input_file}\n")


def coords(arr2d):
    # return [(x0,y0), (x1, y0), ...]
    for y in range(len(arr2d)):
        for x in range(len(arr2d[y])):
            yield (x, y)


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def ans(answer):
    # store answer to clipboard
    from distutils.spawn import find_executable

    xclip_path = find_executable("xclip")
    if xclip_path:
        os.system(f'echo "{answer}"| {xclip_path} -selection clipboard -in')
        print("\t", answer, "| in clipboard\n")
    else:
        print(f"\t {answer} | (answer)\n")


strips = lambda l: list(map(str.strip, l))
ints = lambda l: list(map(int, l))
commas = lambda s: s.split(",")
comma_ints = lambda s: ints(strips(s.split(",")))

L, I, D, S = list, int, dict, set
P, E, R, M = print, enumerate, range, map

############### end of boilerplate #############################################


dirs = {
    "e": (2, 0),
    "w": (-2, 0),
    "se": (1, 1),
    "ne": (1, -1),
    "nw": (-1, -1),
    "sw": (-1, 1),
}


def line_transform(line):
    nu_line = []
    running = ""
    for c in line:
        running += c
        if running in dirs.keys():
            nu_line.append(dirs[running])
            running = ""
    return nu_line


lines = [line_transform(line) for line in lines]  # apply line_transform to each line

tiles = dict()
# tru is black

for idx, line in enumerate(lines):
    x, y = (0, 0)
    for dx, dy in line:
        x, y = x + dx, y + dy
    # print(idx, line)
    cur = tiles.get((x, y), False)
    tiles[(x, y)] = not cur

tot = 0
for k, v in tiles.items():
    if v == True:
        tot += 1
ans(tot)  # 465


neighbor_coords = dirs.values()


def get_neighbor_coords(x, y):
    neighbors = []
    for dx, dy in neighbor_coords:
        xx = x + dx
        yy = y + dy
        neighbors.append((xx, yy))
    return neighbors


def adjacent(_seats, x, y):
    adj = 0
    for xx, yy in get_neighbor_coords(x, y):
        alive = _seats.get((xx, yy), False)
        if alive:
            adj += 1
    return adj


def count(tiles):
    tot = 0
    for _, v in tiles.items():
        if v == True:
            tot += 1
    return tot


for i in range(100):
    to_check = set()
    nu_tiles = deepcopy(tiles)
    for coord, alive in tiles.items():
        # check all tiles touching a live tiles
        if alive:
            to_check.update(set(get_neighbor_coords(coord[0], coord[1])))
            to_check.add(coord)  # do check self
    for coord in to_check:
        alive = tiles.get(coord, False)
        adj = adjacent(tiles, coord[0], coord[1])
        if alive and (adj == 0 or adj > 2):
            nu_tiles[coord] = False
        if not alive and adj == 2:
            nu_tiles[coord] = True
    tiles = nu_tiles
ans(count(tiles))  # 4078

"""
Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
"""

"""
e, se, sw, w, nw, and ne

(0,0) neighbors:

(2,0), e
(-2,0), w
(1,1), se
(1,-1), ne
(-1,-1) nw
(-1,1). sw
"""
