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


def ans(answer):
    # store answer to clipboard
    print(answer, "| in clipboard")
    os.system(f'echo "{answer}"| xclip -selection clipboard -in')


L, I, D, S = list, int, dict, set
P, E, R, M = print, enumerate, range, map

## end of boilerplate ##

SL = lambda arr: list(sorted(arr))


def line_transform(line):
    # split = [line.split() for line in lines]
    # return int(line)
    return [c for c in line]


lines = [line_transform(line) for line in lines]  # apply line_transform to each line
# . floor
# L empty
# # occuipied
import copy

seats = lines
seats_part2 = copy.deepcopy(lines)


def adjacent(_seats, x, y):
    adj = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            yy = y + dy
            xx = x + dx
            if yy < 0 or xx < 0:
                continue
            try:
                if _seats[y + dy][x + dx] == "#":
                    adj += 1
            except:
                # print("bads ", y + dy, x + dx)
                pass
    return adj


import os

import png


def save_as_png(arrs, idx, folder):
    trans = {"L": 0, ".": 150, "#": 255}
    _arrs = copy.deepcopy(arrs)
    for y in range(len(arrs)):
        for x in range(len(arrs[0])):
            _arrs[y][x] = trans[arrs[y][x]]
    if not os.path.exists(folder):
        os.mkdir(folder)
    outfile = os.path.join(folder, str(idx).zfill(5) + ".png")
    png.from_array(_arrs, "L").save(outfile)


# print([[sub[x]for x in (0,7)] for sub in l ])


def nice_print(arrs):
    trans = str.maketrans("L#.", "□■ ")
    ls = ["".join(line).translate(trans) for line in arrs]
    print("\n".join(ls))


def occd(seats):
    tot = 0
    for y in range(len(seats)):
        for x in range(len(seats[0])):
            if seats[y][x] == "#":
                tot += 1
    return tot


def eq(s1, s2):
    for y in range(len(seats)):
        for x in range(len(seats[0])):
            if s1[y][x] != s2[y][x]:
                return False
    return True


def round(_seats):
    nu_seats = copy.deepcopy(_seats)
    for y in range(len(_seats)):
        for x in range(len(_seats[0])):
            # print(adjacent(seats, x, y))
            adj = adjacent(_seats, x, y)
            cur = _seats[y][x]
            if cur == ".":
                continue
            if cur == "L" and adj == 0:
                nu_seats[y][x] = "#"
            if cur == "#" and adj >= 4:
                nu_seats[y][x] = "L"
    return nu_seats


last = occd(seats)
for i in range(5000):
    nice_print(seats)
    save_as_png(seats, i, "pt1_frames")
    nu_seats = round(seats)
    if eq(nu_seats, seats):
        ans(occd(nu_seats))  # 2261
        input("continue to pt 2?")
        break
    seats = nu_seats

## part 2


def visible(_seats, x, y):
    adj = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            step = 1
            yy = y + dy * step
            xx = x + dx * step
            seen = False
            while yy in range(len(_seats)) and xx in range(len(_seats[0])) and not seen:
                if _seats[yy][xx] == "#":
                    adj += 1
                    seen = True
                    break
                elif _seats[yy][xx] == "L":
                    seen = True
                    break
                step += 1
                yy = y + dy * step
                xx = x + dx * step
    return adj


def round2(_seats):
    nu_seats = copy.deepcopy(_seats)
    for y in range(len(_seats)):
        for x in range(len(_seats[0])):
            # print(adjacent(seats, x, y))
            adj = visible(_seats, x, y)
            cur = _seats[y][x]
            if cur == ".":
                continue
            if cur == "L" and adj == 0:
                nu_seats[y][x] = "#"
            if cur == "#" and adj >= 5:
                nu_seats[y][x] = "L"
    return nu_seats


seats = seats_part2
last = occd(seats)
for i in range(500000000):
    save_as_png(seats, i, "pt2_frames")
    nice_print(seats)
    print()
    nu_seats = round2(seats)
    if eq(nu_seats, seats):
        ans(occd(nu_seats))  # 2039
        exit()
    seats = nu_seats
