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


from collections import deque

cups = []
for num in data:
    if num in "\n ":
        continue
    cups.append(int(num))

example = list(map(int, list("389125467")))

if "e" in sys.argv:
    cups = example

PT2 = False
verbose = False
if "v" in sys.argv:
    verbose = True
outer_wheel = []
if "b" in sys.argv or "c" in sys.argv:
    PT2 = True
    max_cup = max(cups)

    biggest_num = 1_000_000
    if "c" in sys.argv:
        biggest_num = 100
    while max_cup < biggest_num:
        max_cup += 1
        outer_wheel.append(max_cup)
        cups.append(max_cup)
    outer_wheel = deque(outer_wheel)


cupset = set(cups)

# Declaring deque
wheel = deque(cups)

max_cup = max(wheel)
deck = deque(cups)

size = len(wheel)


def answer_pt1_wheel(wheel):
    out = []
    one = wheel.index(1)
    print(one)
    for i in range(8):
        out.append((wheel + wheel)[i + one + 1])
    ans("".join(map(str, out)))  # 89372645
    print("ans example 100: 67384529")
    print("ans inp.txt 100: 89372645")


def print_near_one(wheel, surround=10):
    if len(wheel) < 20:
        print(wheel)
        return
    one = wheel.index(1)
    size = len(wheel)
    surround = 10
    # fmt:off
    one_rg = [wheel[i] for i in range(((one+surround) % size)-(surround*2), (one+surround) %size ,1)]
    # fmt:on
    print("L1:", one_rg[:surround])
    print(1, "idx:", one)
    print("R1", one_rg[surround + 1 :])

    # print(wheel)

    pass


printwheel = False
if len(wheel) < 105:
    print(wheel)
# deck = list(deck)
cur_idx = 0
limit = 10_000_000
accessed = set()
if not PT2:  # b to enable bigass numbers
    limit = 100
max_cup = max(wheel)
for iters in range(limit):
    if iters % 100 == 0:
        print(iters)
    cur_val = wheel[0]
    dest_val = cur_val - 1 or max_cup  # avoid 0
    if verbose:
        printwheel = input("-------move: " + str(iters + 1))
        print(f"({wheel[0]})")
        # print(wheel)
    wheel.rotate(-1)
    # cur is WHEEL 0
    # gotta find the dest_val quickly
    # print(f"Cups: {cups}\nval({cur_val})" )
    next_three = [wheel.popleft() for _ in range(3)]
    wheel.rotate(1)  # put cur back at start
    while dest_val in next_three:
        dest_val -= 1
        if dest_val <= 0:
            dest_val = max_cup
    rot_diff = 0
    if verbose:
        dest_idx = wheel.index(dest_val)
        dest_surr = (wheel[dest_idx - 1], dest_val, wheel[(dest_idx + 1) % size])
    while wheel[-1] != dest_val:
        wheel.rotate(-1)
        rot_diff -= 1
        if abs(rot_diff) > 1000:
            exit("bad rotation")
    wheel.extendleft(next_three[::-1])
    wheel.rotate(-rot_diff or -3)
    # print("postrot", wheel, f"({cur_val}) 1st?")
    print("wheel0 ", wheel[0], "cur_val", cur_val)
    assert wheel[0] == cur_val
    # print('idx of VAL', wheel.index(cur_val))
    # print('wheel[0]', wheel[0])
    if verbose == True:
        print("pick up: ", next_three)
        print(f"destination: {dest_val}")

        print("-1, dest, +1", dest_surr)
        print("dest +- 1: ")
        print_near_one(wheel, 10)
        if printwheel:
            print(wheel)
        printwheel = False
    else:
        pass
    next_three = []
    wheel.rotate(-1)
    if iters == 99:
        answer_pt1_wheel(wheel)
    # cur_idx = ( deck.index(cur_val) + 1 ) % size

# insert chunks behind deque onto a separate deck
# i think i need 2 decks
# a center "relevant one"
# the wraparound one which keeps track of 50 to 1 mil
# they'll pop and extend onto each other


# stars = deck[one], deck[one + 1]
# print('idx: ', one, " +1, +2")
# print(stars)
# ans(stars[0] * stars[1])
