import os

# change to dir of script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    with open("input_small.txt") as f:
        data = f.read()  # entire file as string
        lines = data.splitlines()
except:
    print("no input.txt")
    data, lines = "", []

line_groups = data.split("\n\n")  # lines split by double newlines
print(lines)
print(len(lines), "lines in input.txt")


def ans(answer):
    # store answer to clipboard
    print(answer, "| in clipboard")
    os.system(f'echo "{answer}"| xclip -selection clipboard -in')


L, I, D, S = list, int, dict, set
P, E, R, M = print, enumerate, range, map

## end of boilerplate ##


def line_transform(line):
    # split = [line.split() for line in lines]
    # return int(line)
    return line


lines = [line_transform(line) for line in lines]  # apply line_transform to each line

for line in lines:
    pass

start = int(lines[0])
departs = []
waits = []
min_ans = []
small = 1000000

for d in lines[1].split(","):
    if d != "x":
        d = int(d)
        m = d - (start % d)
        print(d, m)
        if m < small:
            print("num small ", small)
            small = m
            print(small, d)
            min_ans.append(small * d)
        waits.append(m)
ans(min_ans[-1])  # 2995

departs = []
offsets = []
for i, d in E(lines[1].split(",")):
    if d != "x":
        d = int(d)
        departs.append(d)
        offsets.append(i)
        print(i)


first = departs[0]
idx = 0

# depart mod clocktime == offset
def allmod(m, l):

    return list(map(lambda e: m % e, l))


def correct_time(time, L):
    corrects = []
    Z = zip(departs, offsets)
    for dep, goal_minute in Z:
        time_away = (time + goal_minute) % dep
        # print(dep, goal_minute, time, time_away)
        if time_away == 0:
            corrects.append(True)
        else:
            corrects.append(False)
    return corrects


def quick_correct(time):
    Z = zip(departs, offsets)
    for dep, goal_minute in Z:
        time_away = (time + goal_minute) % dep
        # print(dep, goal_minute, time, time_away)
        if time_away == 0:
            pass
        else:
            return False
    return True


#      703
a = [0, 1, 2, 3, 4, 5, 6, 7, 8]
print(departs)
print(allmod(first, departs))

marked = dict()
diffs = dict()
for i in range(len(departs)):
    marked[i] = False
while True:
    # CT = correct_time(idx, departs)
    # for i, v in enumerate(CT):
    #     if v:
    #         if not marked[i]:
    #             print(f"{i} depart({departs[i]}) every {idx}")
    #             diffs[i] = idx
    #         marked[i] = True
    # if all(marked.values()):
    #     break
    # if AM[2] == 2:
    #     print(idx - l)
    #     l = idx
    if quick_correct(idx):
        ans(idx)
        exit()
        break
    # if all(correct_time(idx, departs)):
    #     ans(idx)
    #     break
    idx += first
print(diffs.values())

from math import gcd  # Python versions 3.5 and above

# from fractions import gcd # Python versions below 3.5
from functools import reduce  # Python version 3.x


def lcm(denominators):
    return reduce(lambda a, b: a * b // gcd(a, b), denominators)


dv = list(diffs.values())
GOAL_SMALL = 1068781
l = lcm(diffs.values())
s = 1
for i in diffs.values():
    s *= i
    print(GOAL_SMALL / i)
print("multiplied: ", s)
print(correct_time(s, departs))

print("lcm: ", l)
print(correct_time(l, departs))


print("gcd: ", gcd(*dv))
print(correct_time(l, departs))


print("all true below? (1068781)")
print(correct_time(1068781, departs))
