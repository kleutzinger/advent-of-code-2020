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
    return line


lines = [line_transform(line) for line in lines]  # apply line_transform to each line

for idx, line in enumerate(lines):
    pass

# I looked at the paragraph below before I solved this
"""
I did part 1 with just lists, not even deque, but yeah it would take ages for
part 2 to complete. So I redid my solution by implementing a linked list with a
dictionary. Each key is a cup number, and the corresponding value is the next
cup. Moving cups is just a matter of relinking them.
"""


verbose = 0

if "v" in sys.argv:
    verbose = 1
cups = []
for num in data:
    if num in "\n ":
        continue
    cups.append(int(num))
# 614752839

example = list(map(int, list("389125467")))
if "e" in sys.argv:
    cups = example

holder = dict()
million = 10 ** 6
for i in range(1, million):
    holder[i] = i + 1

for idx, label in enumerate(cups[:-1]):
    holder[label] = cups[idx + 1]
holder[cups[-1]] = len(cups) + 1
holder[million] = cups[0]
for c in cups:
    print(c, "->", holder[c])
print(million, "->", holder[million])

max_cup = max(cups)
base = cups[0]  # ()

for i in range(10 * million):
    first = holder[base]
    second = holder[first]
    third = holder[second]
    p = [first, second, third]
    dest_val = base - 1 or max_cup
    while dest_val in p:
        dest_val = dest_val - 1 or max_cup
    if verbose:
        print(f"b({base}) d[{dest_val}] {p}")
        input()
    holder[base] = holder[third]
    holder[third] = holder[dest_val]
    holder[dest_val] = first
    base = holder[base]

first = holder[1]
second = holder[first]
ans(first * second)  # 21273394210
