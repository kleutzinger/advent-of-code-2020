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

p1 = []
p2 = []
groups = data.split("\n\n")
PRINT_OUTPUT = "p" in sys.argv

for idx, p in enumerate(groups):
    for line in p.split("\n")[1:]:
        if line == "":
            continue
        if idx == 0:
            p1.append(int(line))
        else:
            p2.append(int(line))

# for part 2
p1_backup = p1.copy()
p2_backup = p2.copy()

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


def score(deck):
    score = 0
    for idx, c in enumerate(deck[::-1]):
        score += (idx + 1) * c
    return score


print("Winning score (part 1):")
ans(max(score(p1), score(p2)))  # 32472

print("----- Part 2 -----\n")

p1, p2 = p1_backup, p2_backup

if "b" in sys.argv:
    # example input, ans = 291
    p1 = [9, 2, 6, 3, 1]
    p2 = [5, 8, 4, 7, 10]

TOTAL_GAME_COUNT = 1
seen_decks_by_game = dict()

deck2str = lambda d: " ".join(map(str, d))


def print_round(p1, p2, game_num, round_num):
    c1 = p1[0]
    c2 = p2[0]
    s = f"Round {round_num} of Game {game_num}:\n"
    s += f"Player 1's deck: {deck2str(p1)}\n"
    s += f"Player 2's deck: {deck2str(p2)}\n"
    s += f"Player 1 plays : {c1}\n"
    s += f"Player 2 plays : {c2}\n"
    print(s)


# Runs a single round
# give p1 and p2 decks, and a game number
# returns 1, 2, or -1
# returning 1 or 2 is player1/2 winning
# returning -1 means this was a deck combo already seen in this game_num,
#   ending the round and game instantly
def Round(p1, p2, game_num, round_num=1):
    c1, c2 = p1[0], p2[0]
    if PRINT_OUTPUT:
        print_round(p1, p2, game_num, round_num)
    decks = (tuple(p1), tuple(p2))
    seen_already = seen_decks_by_game.get(game_num, set())
    if decks in seen_already:
        # win game by duplication
        return -1
    else:
        seen_already.add(decks)
        seen_decks_by_game[game_num] = seen_already
    if len(p1) <= c1 or len(p2) <= c2:
        # deck too small to recurse, return winner by card
        if c1 > c2:
            return 1
        else:
            return 2
    else:
        # spawn new subgame to determine round winner
        # partial decks:
        p1_sub = p1[1 : c1 + 1]
        p2_sub = p2[1 : c2 + 1]
        # I wonder if there's a way to avoid a global variable
        # game_num=random.random() works probably always
        global TOTAL_GAME_COUNT
        TOTAL_GAME_COUNT += 1
        winner = game(p1_sub, p2_sub, game_num=TOTAL_GAME_COUNT)
        return winner


# Check for an empty deck and return the winning player number
# otherwise return None
def check_victor(p1, p2):
    if len(p1) == 0:
        return 2
    if len(p2) == 0:
        return 1
    return None


# There is a single outer game
# rounds are spawned until p1 or p2 is empty
# subgames may be spawned inside a round to determine a round-winner
# a round may signal a duplicate deck, triggering a game end (p1 win)
# subgames are the same as games, but winning the outer game ends the program
def game(p1, p2, game_num=1):
    game_victor = check_victor(p1, p2)
    round_count = 0
    # runs until p1 or p2 is empty
    while game_victor == None:
        # input(); PRINT_OUTPUT = True ## debug
        round_count += 1
        round_winner = Round(p1, p2, game_num, round_num=round_count)
        if round_winner == -1:
            # duplicate round, end GAME
            return 1
        c1, c2 = p1[0], p2[0]  # topdeck
        p1, p2 = p1[1:], p2[1:]  # remove drawn cards
        if round_winner == 1:
            p1 = p1 + [c1, c2]
        else:
            p2 = p2 + [c2, c1]
        game_victor = check_victor(p1, p2)
    winning_deck = (p1, p2)[game_victor - 1]
    if PRINT_OUTPUT:
        print(f"-- Player {game_victor} wins game {game_num} --\n")
    if game_num == 1:  # outer game
        print(f"Overall winner: Player {game_victor}")
        print(f"Final deck:\n{deck2str(winning_deck)}")
        print(f"Total nested game count: {TOTAL_GAME_COUNT:,}")
        total_rounds = sum([len(i) for i in seen_decks_by_game.values()])
        print(f"Total rounds played: {total_rounds:,}")
        print("Winning score:")
        ans(score(winning_deck))  # 36463
    return game_victor


# spawn outer game to find answer
game(p1, p2, game_num=1)

# not 34625
# not 33417
# not 31540
# not 32058
