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
# print(lines)
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

L, I, D, S = list, int, dict, set
P, E, R, M = print, enumerate, range, map

############### end of boilerplate #############################################


def line_transform(line):
    # split = [line.split() for line in lines]
    # return int(line)
    return line


lines = [line_transform(line) for line in lines]  # apply line_transform to each line

lg = data.split("\n\n")
r1 = dict()
r2 = dict()
for line in line_groups[0].split("\n"):
    l, r = line.split(":")
    for idx, out in E(r.split("|")):
        l = int(l)
        out = out.strip()
        if '"' in out:
            out = out[1]
            print(l, ":", out)
            r1[l] = [out]
            continue
        else:
            out = out.split(" ")
        if idx == 0:
            r1[l] = ints(out)
        if idx == 1:
            r2[l] = ints(out)
print(list(r1.items()))


# base case: all terminals, return
# recursive case:
#   branch down each path


# exit()
# print(parents(0))
i = 0
cur = ""
terminated = []


def all_terminals(L):
    return all([type(r) == str for r in L])


def find_rewrite(guys=[]):
    if all_terminals(guys):
        return guys
    rewritten = False
    nu_guys = []
    for idx, c in E(guys):
        if type(c) == str:
            pass
        rewrite1 = r1.get(c, [])
        if rewrite1:
            rewritten = True
            rw = guys[:idx] + rewrite1 + guys[idx + 1 :]
            nu_guys.append(rw)
        rewrite2 = r2.get(c, [])
        if rewrite2:
            rewritten = True
            rw = guys[:idx] + rewrite2 + guys[idx + 1 :]
            nu_guys.append(rw)
        if rewritten:
            return nu_guys


# [4,1,5]
# [["a", 2, 3, 5], ["a", 3, 2, 5]]

# ["a", 2, 3, "b"]
# ["a", 4, 4, 4, 5]
all_guys = set()


def traverse(guys):
    if all_terminals(guys):
        s = "".join(map(str, guys))
        all_guys.add(s)
    else:
        children = find_rewrite(guys)
        for c in children:
            # print(c)
            traverse(c)


traverse([0])
# print(all_guys)
tot = 0
for line in line_groups[1].split("\n"):
    if line in all_guys:
        tot += 1
    else:
        print(line, "not in")
ans(tot)  # 113
# base case: all terminals, return
# recursive case:
#   branch down each path
