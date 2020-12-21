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
print(f"{len(lines)} lines in {input_file}\n")


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
    print(answer, "| in clipboard\n")
    os.system(f'echo "{answer}"| xclip -selection clipboard -in')


strips = lambda l: list(map(str.strip, l))
ints = lambda l: list(map(int, l))
commas = lambda s: s.split(",")
comma_ints = lambda s: ints(strips(s.split(",")))

L, I, D, S = list, int, dict, set
P, E, R, M = print, enumerate, range, map

############### end of boilerplate #############################################


def line_transform(line):
    left, right = line.split(" (contains ")
    right = right[:-1]
    return left.split(" "), right.split(", ")


lines = [line_transform(line) for line in lines]  # apply line_transform to each line

english_words = set()
candidates = dict()


l_sets = []
r_sets = []
for idx, line in enumerate(lines):
    gibberish, english = line
    for e in english:
        english_words.add(e)
    l_sets.append(set(gibberish))
    r_sets.append(set(english))

for english_word in english_words:
    possible_translations = []
    for l, r in zip(l_sets, r_sets):
        if english_word in r:
            possible_translations.append(l)
    intersect = set.intersection(*possible_translations)
    candidates[english_word] = intersect
    spacer = " " * (9 - len(english_word))
    print(english_word, spacer + "∈", intersect)

# below is similar to my solution for the ticketing problem
done = False
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
        # all english words have a single translation
        done = True

print()

for e in english_words:
    arrow = "-" * (9 - len(e)) + ">"
    print(e, arrow, list(candidates[e])[0])

dangerous_gibberish = set()
for gib in candidates.values():
    dangerous_gibberish.update(gib)

tot = 0
for left, _ in lines:
    for gib in left:
        if gib not in dangerous_gibberish:
            tot += 1

print("\nnumber of non-dangerous ingredients:")
ans(tot)  # 2061

s = list(sorted([e for e in english_words]))
s = [candidates[e].pop() for e in s]
s = ",".join(s)
print("killer ingredients sorted by their english translation:")
ans(s)  # cdqvp,dglm,zhqjs,rbpg,xvtrfz,tgmzqjz,mfqgx,rffqhl

# this problem was kind of poorly written. it was the same as the
# ticket-numbering problem, but the wording was pretty off this time. it didn't
# seem like there was a one-to-one correspondence between allergens and
# ingredients. the wording made it sound like nskl and xbxcvz could both contain
# milk. part 2 was somewhat trivial, really, but after yesterday's monster
# hunting, I'm not complaining.
