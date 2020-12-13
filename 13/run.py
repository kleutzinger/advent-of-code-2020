import os

# change to dir of script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    with open("input.txt") as f:
        # with open("input_small.txt") as f:
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

## part 2 ##

departs = []
offsets = []
offsets2 = []
offsets3 = []
for i, d in enumerate(lines[1].split(",")):
    if d != "x":
        d = int(d)
        departs.append(d)
        offsets.append(i)
        while i > d:
            i -= d
        offsets2.append(i)
        offsets3.append(d - i)
        print(i)


first = departs[0]
idx = 0

from math import gcd  # Python versions 3.5 and above

# depart mod clocktime == offset
def allmod(m, l):
    return list(map(lambda e: m % e, l))


def correct_time(time, L=departs):
    # show buses at correct time + offset
    # return [True, False, False, ...]
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
    # quickly show if time is correct
    # return True/False
    Z = zip(departs, offsets)
    for dep, goal_minute in Z:
        time_away = (time + goal_minute) % dep
        # print(dep, goal_minute, time, time_away)
        if time_away == 0:
            pass
        else:
            return False
    return True


Z = list(zip(departs, offsets3))
eqn = "solve for x, "
# eqn = ""
for dep, offset in Z:
    eqn += f"x = {dep - offset} mod {dep}, "
print(eqn)  # me trying to make a wolfram alpha query post

from functools import reduce

# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


n = departs[:]
a = offsets3[:]
# print("1068781, correct small_input")
cr = chinese_remainder(n, a)
ans(cr)  # 1012171816131114
exit()

"""
wrong attempts below
"""
#      703

# a = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# print(departs)
# print(allmod(first, departs))

# marked = dict()
# diffs = dict()
# for i in range(len(departs)):
#     marked[i] = False
# while True:
#     # CT = correct_time(idx, departs)
#     # for i, v in enumerate(CT):
#     #     if v:
#     #         if not marked[i]:
#     #             print(f"{i} depart({departs[i]}) every {idx}")
#     #             diffs[i] = idx
#     #         marked[i] = True
#     # if all(marked.values()):
#     #     break
#     # if AM[2] == 2:
#     #     print(idx - l)
#     #     l = idx
#     if quick_correct(idx):
#         ans(idx)  # this will theoretically finish
#         exit()
#         break
#     # if all(correct_time(idx, departs)):
#     #     ans(idx)
#     #     break
#     idx += first
# print(diffs.values())

# # from fractions import gcd # Python versions below 3.5
# from functools import reduce  # Python version 3.x


# def lcm(denominators):
#     return reduce(lambda a, b: a * b // gcd(a, b), denominators)


# dv = list(diffs.values())
# GOAL_SMALL = 1068781
# l = lcm(diffs.values())
# s = 1
# for i in diffs.values():
#     s *= i
#     print(GOAL_SMALL / i)
# print("multiplied: ", s)
# print(correct_time(s, departs))

# print("lcm: ", l)
# print(correct_time(l, departs))


# print("gcd: ", gcd(*dv))
# print(correct_time(l, departs))


# print("all true below? (1068781)")
# print(correct_time(1068781, departs))
