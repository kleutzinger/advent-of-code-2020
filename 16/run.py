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


L, I, D, S = list, int, dict, set
P, E, R, M = print, enumerate, range, map

############### end of boilerplate #############################################


def line_transform(line):
    # split = [line.split() for line in lines]
    # return int(line)
    return line


lines = [line_transform(line) for line in lines]  # apply line_transform to each line

top, middle, bottom = line_groups


def or_to_range(s):
    s = s.strip()
    l, r = s.split("-")
    return range(int(l), int(r) + 1)


all_ranges = set()  # {all possible ranges}
rules = dict()  # field -> (range1, range2)
for line in top.split("\n"):
    rule_field, ranges = line.split(":")
    r1, r2 = ranges.split("or")
    r1, r2 = or_to_range(r1), or_to_range(r2)
    print(rule_field, r1, r2)
    rules[rule_field] = (r1, r2)
    all_ranges.add(r1)
    all_ranges.add(r2)

my_nums = []
for num in middle.split("\n")[1].split(","):
    num = int(num)
    my_nums.append(num)

invalid_total = 0
valid_tickets = []
for ticket in bottom.split("\n")[1:-1]:
    all_valid = True
    for num in ticket.strip().split(","):
        num = int(num)
        valid = False
        for rule in all_ranges:
            if num in rule:
                valid = True
        if not valid:
            all_valid = False
            invalid_total += num
    if all_valid:
        ticket = [int(poss) for poss in ticket.strip().split(",")]
        valid_tickets.append(ticket)

ans(invalid_total)  # 20048

## part 2 ##

possible_locs = dict()

print("number of valid tickets: ", len(valid_tickets))
for (rule_idx, (rule_field, (r1, r2))) in enumerate(rules.items()):
    # loop through rules
    # tidx is column idx for ticket vals
    for tidx in range(len(valid_tickets[0])):
        # tidx_vals = all ticket values at column tidx
        tidx_vals = [t[tidx] for t in valid_tickets]
        # check if entire column is valid for current rule
        if all([(tv in r1) or (tv in r2) for tv in tidx_vals]):
            # merge candidate column index into this rule
            already = deepcopy(possible_locs.get(rule_field, set()))
            already.add(tidx)
            possible_locs[rule_field] = already
# we now have a dict mapping rule -> set{possible_column_idxs}
print(possible_locs)

done = False
discarded = set()  # set of processed singletons
while not done:
    # loop through all rules looking for singletons
    for rule_field in possible_locs.keys():
        # poss is the set of possible columns at current rule
        poss = possible_locs[rule_field]
        if len(poss) == 1 and not poss.issubset(discarded):
            print("new singleton found ", poss)
            nu_dict = deepcopy(possible_locs)
            for kinner, sinner in possible_locs.items():
                # discard singleton from all other sets
                if kinner != rule_field:
                    nu_dict[kinner] = sinner - poss
            # add singleton to set of processed singletons
            discarded = discarded.union(poss)
            possible_locs = nu_dict
            # print(nu_dict)
            if all([len(s) == 1 for s in possible_locs.values()]):
                # all rules have a single column
                done = True
            break


my_ticket = []
for ticket in middle.split("\n")[1:]:
    for num in ticket.strip().split(","):
        my_ticket.append(int(num))

print(possible_locs)
deptot = 1
for k, poss in possible_locs.items():
    if k.startswith("departure"):
        idx = poss.pop()
        deptot *= my_ticket[idx]
ans(deptot)  # 4810284647569
# not 674193590767
