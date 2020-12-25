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


def line_transform(line):
    # split = [line.split() for line in lines]
    # return int(line)
    return int(line)


lines = [line_transform(line) for line in lines]  # apply line_transform to each line

for idx, line in enumerate(lines):
    print(line)
    pass


a, b = lines
mod = 20201227

door_pub = a
card_pub = b


def trans(sub, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= sub
        value = value % mod
    return value


def find(sub, goal):
    value = 1
    for i in range(10 ** 10):
        value *= sub
        value = value % mod
        if value == goal:
            return i + 1
    return None


door_loop = find(7, a)
card_loop = find(7, b)
secret = trans(door_pub, card_loop)
secret2 = trans(card_pub, door_loop)
ans(secret)  # 1478097
ans(secret2)  # 1478097

print(f)
