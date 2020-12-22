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
    # split = [line.split() for line in lines]
    # return int(line)
    return line


p1 = []
p2 = []
groups = data.split("\n\n")

for idx, p in E(groups):
    for line in p.split("\n")[1:]:
        print(line)
        if line == "":
            continue
        if idx == 0:
            p1.append(int(line))
        else:
            p2.append(int(line))

pp1 = deepcopy(p1)
pp2 = deepcopy(p2)
print(len(p1), len(p2))

while True:
    c1, c2 = p1[0], p2[0]
    p1 = p1[1:]
    p2 = p2[1:]
    bigger, smaller = max(c1, c2), min(c1, c2)
    if c1 > c2:
        p1.extend([bigger, smaller])
    else:
        p2.extend([bigger, smaller])
    if len(p1) * len(p2) == 0:
        break

print(p1, p2)


def score(deck):
    score = 0
    for idx, c in E(deck[::-1]):
        score += (idx + 1) * c
    return score


ans(max(score(p1), score(p2)))  # 32472

# same decks: win for p1

played = set()
l1 = []
l2 = []

p1 = pp1
p2 = pp2
if "b" in sys.argv:
    p1 = [9, 2, 6, 3, 1]
    p2 = [5, 8, 4, 7, 10]

if "c" in sys.argv:
    p1 = [43, 19]
    p2 = [2, 29, 14]


import random

GAME_COUNT = 1
seen_decks_by_game = dict()


def Round(p1, p2, ROUND=1, GAME=None):
    c1, c2 = p1[0], p2[0]
    s = f"""
    ROUND {ROUND} of {GAME}
    Player 1's deck: {p1}
    Player 2's deck: {p2}
    Player 1 plays: {c1}
    Player 2 plays: {c2} """
    if "p" in sys.argv:
        print(s)
    decks = (tuple(p1), tuple(p2))
    seen_already = seen_decks_by_game.get(GAME, set())
    if decks in seen_already:
        # print("p1 wins by duplication")
        return -1
    else:
        seen_already.add(decks)
        seen_decks_by_game[GAME] = seen_already
        # print(len(seen_already))
    # p1 = p1[1:].copy()
    # p2 = p2[1:].copy()
    ROUND += 1
    if len(p1) <= c1 or len(p2) <= c2:
        # cant recurse
        # print('cant recurse')
        if c1 > c2:
            return 1
        else:
            return 2
    # recurse game
    # pop cards here?
    else:
        # print(f'recursing depth: {GAME}')
        dd1 = p1[1 : c1 + 1]
        dd2 = p2[1 : c2 + 1]
        global GAME_COUNT
        GAME_COUNT += 1
        winner = game(dd1, dd2, inner=True, GAME=GAME_COUNT)
        # print(f'end depth: {GAME}')

        return winner


# round returns 1 or 2 simply
# might have to recurse into a game
# to determine this, though
def len_win(p1, p2):
    if len(p1) == 0:
        return 2
    if len(p2) == 0:
        return 1
    return None


smallest_ever = len(p1)


def game(p1, p2, inner=True, GAME=1):
    # runs until p1 or p2 is empty
    game_victor = len_win(p1, p2)
    round_count = 0
    global GAME_COUNT
    while game_victor == None:
        # input()
        round_count += 1
        round_winner = Round(p1, p2, ROUND=round_count, GAME=GAME)
        if round_winner == -1:
            # duplicate round, end GAME
            return 1
        c1, c2 = p1[0], p2[0]  # draw card
        p1, p2 = p1[1:], p2[1:]  # pop drawn card
        # print(f"Player {round_winner} wins round {round_count}")

        if round_winner == 1:
            p1 = p1 + [c1, c2]
        else:
            p2 = p2 + [c2, c1]
        game_victor = len_win(p1, p2)
    winning_deck = [0, p1, p2][game_victor]
    if inner == False:
        print(game_victor)
        print(winning_deck)
        ans(score(winning_deck))  # 36463
        exit()
    if "p" in sys.argv:
        print(f"player {game_victor} wins game {GAME}")
    return game_victor


print(p1, p2)
print(game(p1, p2, inner=False, GAME=1))

# ans(max(score(p1), score(p2)))
# not 34625
# not 33417
# not 31540
# not 32058
