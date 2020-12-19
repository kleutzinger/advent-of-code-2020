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

# {int : [int|str, int|str, ...]}
# int => nonterminal, str => terminal
r1 = dict()  # first rewrite rules
r2 = dict()  # optional right side of pipe rewrite rules

# this is for part 2
add_me = """
8: 42 | 42 8
11: 42 31 | 42 11 31"""
nu_grup = line_groups[0] + add_me

for line in nu_grup.split("\n"):
    # set up rewrite rules
    l, r = line.split(":")
    for idx, out in E(r.split("|")):
        l = int(l)
        out = out.strip()
        if '"' in out:
            out = out[1]
            r1[l] = [out]
            continue
        else:
            out = out.split(" ")
        if idx == 0:
            r1[l] = ints(out)
        if idx == 1:
            r2[l] = ints(out)
print(list(r1.items()), "\n\n", list(r2.items()))


def all_terminals(L):
    # check if list L only contains terminals
    return all([type(r) == str for r in L])


def find_rewrite(guys=[]):
    # find one or two possible rewrites for a
    # list of terminals and nonterminals.
    # it finds the first nonterminal left to right
    # returns a list of 1 or 2 rewrites based on that nonterminal
    # (1 or 2 depending if its rewrite rule has a pipe in it)
    # returns None if list contains no nonterminals
    rewritten = False
    nu_guys = []
    for idx, c in enumerate(guys):
        if type(c) == str:
            # terminal found, continue search
            continue
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


notes = """
0: 8 11
8:  42    | 42 8
11: 42 31 | 42 11 31
# pretend:
42:  A
31 : B

8:  A   | A 8
11: A B | A 11 B

0: A+AB+
where: B_count <= A_count
"""

all_guys = set()
longest_in_set = lambda s: 0 if len(s) == 0 else max([len(i) for i in s])


def traverse(guys, store=all_guys):
    # add possible terminals from a starting list to a global set `store`
    # this can get stuck in a loop, as it is greedy
    # keep finding rewrites a starting point's children and add them to a set
    if all_terminals(guys):
        s = "".join(map(str, guys))
        store.add(s)
    else:
        children = find_rewrite(guys)
        # input(children)
        for c in children:
            traverse(c)


# find all terminals from the two special numbers
# these two numbers are directly reachable from [0]
# [0] has infinite loops, so we cannot traverse it directly
traverse([42])
sA = all_guys.copy()
all_guys.clear()
traverse([31])
sB = all_guys.copy()


def to_chunks(st, size=8):
    # "0123456701234567" -> ["01234567","01234567"]
    import textwrap

    return textwrap.wrap(st, size)


def transform(st):
    # transform given lines into AAABB strings
    # set A is the set of terminals reachable by [42]
    # set B is the set of terminals reachable by [31]
    # these sets are disjoint and contain only strings of length 8
    # each given line should be made up of these two sets
    # in chunks of 8
    l = len(list(sA)[0])
    chunks = to_chunks(st, l)
    nu_str = ""
    for chunk in chunks:
        if chunk in sA:
            nu_str += "A"
        elif chunk in sB:
            nu_str += "B"
        else:
            nu_str += "X"
    return nu_str


def verify(st):
    # A+AB+ where there is more A than B
    if len(st) < 3:
        # print("bad1 len < 3", st)
        return False
    if st[:2] != "AA":
        # print("bad2 no AA start", st)
        return False
    bidx = st.find("B")
    if bidx == -1:
        # print("bad3 no B in string", st)
        return False
    if "A" in st[bidx:]:
        # print("bad4 A after B", st)
        return False
    if st.count("B") >= st.count("A"):
        # print("bad5 B_count >= A_count", st)
        return False
    return True


tot = 0
for line in line_groups[1].split("\n")[:-1]:
    line = transform(line)
    valid = verify(line)
    # input((valid, line)) # debug
    if valid:
        tot += 1
        print(str(tot).zfill(3), line)
    else:
        print("XXX", line)
ans(tot)  # 253
# not 268 ( too high)
