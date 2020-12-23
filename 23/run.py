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
    print(xclip_path)
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

cups = []
for num in data:
    if num in "\n ":
        continue
    cups.append(int(num))

print(cups)
example = list(map(int, list("389125467")))


def move(cups=cups, cur_idx=0):
    max_cup = max(cups)
    cur_val = cups[cur_idx]
    print(f"Cups: {cups}\nval({cur_val})")
    size = len(cups)
    next_three = []
    for i in (1, 2, 3):
        nidx = (cur_idx + i) % size
        next_three.append(cups[nidx])
    for i in next_three:
        cups.remove(i)
    dest_val = cur_val - 1
    while dest_val not in cups:
        dest_val -= 1
        if dest_val <= 0:
            dest_val = 9
    print(f"Pick up: {next_three}")
    print(f"destination {dest_val}")
    dest_idx = cups.index(dest_val)
    for i, v in E(next_three):
        into = dest_idx + i + 1
        cups.insert(into, v)
    new_idx = (cups.index(cur_val) + 1) % size
    return cups, new_idx


cups = cups
idx = 0
for i in range(100):
    print(f"-- move {i+1} --")
    cups, idx = move(cups, idx)

print(cups)

out = []
one = cups.index(1)
print(one)
for i in range(8):
    out.append((cups + cups)[i + one + 1])

ans("".join(map(str, out)))  # 89372645
