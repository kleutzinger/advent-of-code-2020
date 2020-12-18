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
print(lines)
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


def line_transform(line):
    # split = [line.split() for line in lines]
    # return int(line)
    return line


lines = [line_transform(line) for line in lines]  # apply line_transform to each line


def mark_depth(s):
    # return a list of paren-depth of all indexes
    #  in:  "1 + (2 * 3) + (4 * (5 + 6))"
    #  out: [000011111100001111122222210] (commas ommitted)
    stack = []
    depth = 0
    for c in s:
        if c == "(":
            depth += 1
        if c == ")":
            depth -= 1
        stack.append(depth)
    return stack


def innermost_idxs(s):
    # return start and end idxs of the innermost parentheses section
    # in: "1 + (2 * 3) + (4 * (5 + 6))"
    # out: (19, 25)           ^     ^
    depths = mark_depth(s)
    maxd = max(depths)
    end = len(s) - 1
    start = -1
    for i, v in enumerate(depths):
        if v == maxd and start == -1:
            start = i
            continue
        if v != maxd and start != -1:
            end = i
            break
    return start, end


def tokenize(s):
    # assume no parentheses
    # tokenize expression into [1, '*', 3, ...]
    # weird logic, but it works
    chunks = s.split(" ")
    relevant_chunks = []
    for chunk in chunks:
        try:
            i = int(chunk)
        except:
            i = None
        if i != None:
            relevant_chunks.append(i)
            continue
        if "*" in chunk:
            relevant_chunks.append("*")
            continue
        if "+" in chunk:
            relevant_chunks.append("+")
            continue
        if "-" in chunk:
            relevant_chunks.append("-")
            continue
    return relevant_chunks


def calc(tokens, part2=True):
    # assume no parentheses
    # outputs a single value from a token-list with [num, +, -, *]
    while "+" in tokens and part2:
        plus_idx = tokens.index("+")
        l = tokens[plus_idx - 1]
        r = tokens[plus_idx + 1]
        added = l + r
        tokens = tokens[: plus_idx - 1] + [added] + tokens[plus_idx + 2 :]
    # plus signs are evaluated and removed
    # eval the rest now
    running_val = None
    op = None
    for c in tokens:
        if type(c) == int:
            # found a number
            if op == None:
                running_val = c
            elif op == "+":
                running_val += c
            elif op == "-":
                running_val -= c
            elif op == "*":
                running_val *= c
        else:
            # found an operator
            op = c
    return running_val


def eval2(s):
    # assume no parentheses
    # evaluate a simple expression string
    tokens = tokenize(s)
    calcd = calc(tokens)  # change for for part 1 ans
    return calcd


def repl_innermost(expr):
    # this is the killer function
    # eliminate innermost parentheses by evaluating it and replacing it
    # return a new expression
    # in:  `1 + (1 + (2 + 2))`
    # out: `1 + (1 + 4)`
    start, end = innermost_idxs(expr)
    # inner = innermost_expression
    inner = expr[start : end + 1]
    inner = inner.replace("(", " ").replace(")", " ")
    inner_val = str(eval2(inner))
    expr = expr[:start] + inner_val + expr[end + 1 :]
    return expr


total = 0
for line in lines:
    expr = line
    while "(" in expr:
        # elim parens
        expr = repl_innermost(expr)
    # eval simple expression
    result = eval2(expr)
    print(" ".join(map(str, (eval2(expr), "=", line))))
    total += result


# ans(total)  # 5374004645253 (part 1)
# (change calc function to get pt 1)

ans(total)  # 88782789402798 (part 2)
