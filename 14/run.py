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

line_groups = data.split("\n\n")  # lines split by double newlines
print(lines)
print(len(lines), "lines in input.txt")


def coords(arrs):
    coords = []
    for y in range(len(arrs)):
        for x in range(len(arrs[0])):
            coords.append((x, y))
    return coords


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
    l, r = line.split("=")
    l = l.strip()
    r = r.strip()
    return (l, r)


lines = [line_transform(line) for line in lines]  # apply line_transform to each line


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def maskbits(mask, num):
    ones = find(mask, "1")
    zeroes = find(mask, "0")
    # print(ones, zeroes)
    bnum = bin(num)[2:].zfill(36)
    # print(len(bnum))
    bits = list(bnum)
    for i in ones:
        bits[i] = "1"
    for i in zeroes:
        bits[i] = "0"

    return int("".join(bits), 2)


mem = dict()

for l, r in lines:
    # print(l, r)
    if l.startswith("mask"):
        mask = r
    else:
        # write to mem[x]
        val = int(r)
        addr = int(l[4 : l.find("]")])
        print(addr)
        write_val = maskbits(mask, val)
        mem[addr] = write_val

ans(sum(mem.values()))  # 13476250121721

## part 2 ##


from itertools import chain, combinations


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


import copy

num2bin = lambda num: bin(num)[2:].zfill(36)


def apply_premask(b, mask):
    ones = find(mask, "1")
    xs = find(mask, "X")

    # print(ones, zeroes)
    bnum = num2bin(b)
    # print(len(bnum))
    bits = list(bnum)
    for i in ones:
        bits[i] = "1"
    for i in xs:
        bits[i] = "X"
    return "".join(bits)


def generation_x(bin_str):
    # 10XX -> [1000, 1001, 1010, 1011]
    xidx = find(bin_str, "X")
    og_bits = list(bin_str)
    for i in xidx:
        og_bits[i] = "0"
    pool = []
    for write_to in powerset(xidx):
        bits = copy.deepcopy(og_bits)
        for loc in write_to:
            bits[loc] = "1"
        pool.append("".join(bits).zfill(36))
    return pool


mask2idx = lambda m: int(m, 2)

mem = dict()
line = 0
for l, r in lines:
    line += 1
    print("line ", line)
    # print(l, r)
    if l.startswith("mask"):
        premask = r
    else:
        val = int(r)
        addr = int(l[4 : l.find("]")])
        xaddr = apply_premask(addr, premask)
        # print("nu:", addr, premask, xaddr)
        for addr in generation_x(xaddr):
            # print(addr, mask2idx(addr), val)
            mem[addr] = val

ans(sum(mem.values()))  # 4463708436768
# not 657193787449
# not 1804269557402

"""
my memory items are like this for pt 2:
('100100000110011001010001111001111100',409649) but that doesn't really
negatively affect anything. pretty fun problem, but i pretty fun problem, but i
wish I could have worked in some bitwise operator usage
"""
