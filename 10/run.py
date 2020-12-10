"""
I was barking up the wrong tree for most of this part 2
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
print("\n\n")


def ans(answer):
    # store answer to clipboard
    print(answer, "| in clipboard")
    os.system(f'echo "{answer}"| xclip -selection clipboard -in')


L, I, D, S = list, int, dict, set
P, E, R, M = print, enumerate, range, map
## end of boilerplate


def line_transform(line):
    # split = [line.split() for line in lines]
    return int(line)


line_groups = data.split("\n\n")  # lines split by double newlines
lines = [line_transform(line) for line in lines]  # apply line_transform to each line

srtd = sorted(lines)  # integers
print(srtd)

ones = 1
threes = 1
for idx, j in E(srtd):
    if idx == 0:
        continue
    diff = j - srtd[idx - 1]
    if diff == 1:
        ones += 1
    elif diff == 3:
        threes += 1
    else:
        print(diff)
    # print(diff)

print(ones, threes)
ans(ones * threes)  # 2760

## part 2

paths = dict()
paths[0] = 1
paths[1] = 1

for s in srtd:
    m1 = s - 1
    m2 = s - 2
    m3 = s - 3
    cnt = 0
    cnt += paths.get(m1, 0)
    cnt += paths.get(m2, 0)
    cnt += paths.get(m3, 0)
    paths[s] = cnt
print(paths)
ans(paths[186])  # 13816758796288

## elegant re-write
paths = dict({0: 1})
for s in srtd:
    paths[s] = sum([paths.get(s - d, 0) for d in [1, 2, 3]])
ans(paths[srtd[-1]])  # 13816758796288


"""
everything below is me going way too crazy trying to figure
out a recursive solution to a pretty simple problem.
It was an interesting thing I was working on, it just was not
required for this problem. the solution was really just
smart counting / a statistical approach.
It's also double-wrong because I was looking for ways to traverse
only by ones and threes, which was not a constraint for part 2.
(it was ones, twos, and threes)

"""
from itertools import combinations

comb = combinations


m = 189
z = 0

# [0]
#   [0, 1]
#   [0, 3]

# recursive case
# none present: return 0
# one present add sum of that branch
# both present add sum of the other branch
# reach final index how many ways
# base case:
# how many ways are there to get to goal from previous numbers
# but only by increments of 1 and 3

# how many ways to reach from val to goal


# reach val to goal
def reach(goal, pool, ways=0):
    print("reach: ", goal, "\nwith: ", pool, "\nthusfar", ways, "\n\n")
    # if goal in memo_cache:
    #     return memo_cache[goal]
    m3 = goal - 3
    m1 = goal - 1
    # base case is if m1 or m3 equals one or 3
    if m3 in pool and m1 in pool:
        # ways += 2
        print("both")
        d1 = pool.copy()
        d3 = pool.copy()
        d1.discard(m1)
        d3.discard(m3)
        s1 = reach(m1, d1, ways + 2)
        s2 = reach(m3, d3, ways + 2)
        return 2 + s1 + s2
    elif m3 in pool:
        print("just m3")
        # just m3 in pool
        drained = pool.copy()
        drained.discard(m3)
        return 1 + reach(m3, drained, ways + 1)
    elif m1 in pool:
        print("just m1")
        # just m1 in pool
        drained = pool.copy()
        drained.discard(m1)
        return 1 + reach(m1, drained, ways + 1)
    else:
        print("no way")
        # no more ways to count down
        return 0


memo_cache = dict()

# print(reach(3, set([1, 2, 3])))

# cap = 4
# for s in reversed(srtd[:4]):
#     cur = reach(s, set(srtd[:4]))
#     memo_cache[s] = cur
#     print(s, cur)
# print(memo_cache)

# print(memo_cache)
# how many ways to reach 189?
# recursive case: 189 - 3 or 189 - 1
# base case: pool = 3 or 1
pool = set(srtd)
pool.add(0)
pres = []
