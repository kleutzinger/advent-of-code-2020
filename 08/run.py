"""
This was a fun problem, and I was able to solve it quickly
It was almost an infinite loop checker, in some ways
maybe it's an infinite-loop-avoider
It makes me wonder actually about error correction
on machine code. Can ASM survive a bit flip?
"""
import os

# change to dir of script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    with open("input.txt") as f:
        data = f.read()  # entire file as string
        lines = data.splitlines()
except:
    print("no input.txt")
    data, lines = "", []

print(lines)
print(len(lines), "lines in input.txt")


def ans(answer):
    # store answer to clipboard
    print(answer, "| in clipboard")
    os.system(f'echo "{answer}"| xclip -selection clipboard -in')


def line_transform(line):
    # split = [line.split() for line in lines]
    return line.split(" ")


line_groups = data.split("\n\n")  # lines split by double newlines
lines = [line_transform(line) for line in lines]  # apply line_transform to each line

L, I, D, S = list, int, dict, set
P, E, R, M = print, enumerate, range, map
## end of boilerplate

acc = 0
idx = 0
visited = set()
while True:
    cur = lines[idx]
    ins, val = cur
    visited.add(idx)
    if ins == "acc":
        acc += int(val)
        idx += 1
    elif ins == "nop":
        idx += 1
    elif ins == "jmp":
        idx += int(val)
    if idx in visited:
        break
ans(acc)  # 1179


def try_chg(lines):
    acc = 0
    idx = 0
    visited = set()
    while True:
        cur = lines[idx]
        ins, val = cur
        visited.add(idx)
        if ins == "acc":
            acc += int(val)
            idx += 1
        elif ins == "nop":
            idx += 1
        elif ins == "jmp":
            idx += int(val)
        if idx in visited:
            return False
        if idx >= len(lines) - 1:
            return acc


import copy

for i, line in enumerate(copy.deepcopy(lines)):
    newlines = copy.deepcopy(lines)
    if line[0] == "nop":
        newlines[i][0] = "jmp"
    elif line[0] == "jmp":
        newlines[i][0] = "nop"
    if try_chg(newlines) != False:
        ans(try_chg(newlines))  # 1089
