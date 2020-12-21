############### boilerplate ####################################################
import os
import sys
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
print(len(lines), "lines in", input_file)


def coords(arr2d):
    # return [(x0,y0), (x1, y0), ...]
    coords = []
    for y in range(len(arr2d)):
        for x in range(len(arr2d[y])):
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
    left, right = line.split(" (contains ")
    right = right[:-1]
    return left.split(" "), right.split(", ")


lines = [line_transform(line) for line in lines]  # apply line_transform to each line

english_words = set()
candidates = dict()

gibb = []
eng = []

l_sets = []
r_sets = []
for idx, line in enumerate(lines):
    ingr, allg = line
    for a in allg:
        english_words.add(a)
    l_sets.append(set(ingr))
    r_sets.append(set(allg))
    gibb.append(ingr)
    eng.append(allg)
    print(ingr, allg)

for english_word in english_words:
    possible_translations = []
    for l, r in zip(l_sets, r_sets):
        if english_word in r:
            possible_translations.append(l)
    intersect = set.intersection(*possible_translations)
    candidates[english_word] = intersect
    print(english_word, intersect)


done = False
a_discard = False
discarded = set()
while not done:
    for english_word, gset in candidates.items():
        if len(gset) == 1 and not english_word in discarded:
            for kinner, sinner in candidates.items():
                if kinner != english_word:
                    candidates[kinner] = sinner - gset
            discarded.add(english_word)
            break
    if all([len(s) == 1 for s in candidates.values()]):
        # all rules have a single column
        done = True
allergens = set()
for i in candidates.values():
    allergens.update(i)
tot = 0
for left, r in lines:
    for ing in left:
        if ing not in allergens:
            tot += 1
ans(tot)  # 2061

s = list(sorted([e for e in english_words]))
s = [candidates[i].pop() for i in s]
s = ",".join(s)
ans(s)  # cdqvp,dglm,zhqjs,rbpg,xvtrfz,tgmzqjz,mfqgx,rffqhl
