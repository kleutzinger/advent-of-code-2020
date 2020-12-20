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

tiles = {}
for tile in data.split("\n\n"):
    tile = tile.strip()
    tile_lines = tile.split("\n")
    _id = tile_lines[0].split("Tile ")[1][:-1]
    _id = int(_id)
    squares = []
    for line in tile_lines[1:]:
        line = [i == "#" for i in line]
        squares.append(line)
    tiles[_id] = squares
# print(list(tiles.items()))


def top(t):
    return t[0]


def bot(t):
    return t[-1]


def left(t):
    return [t[i][0] for i in range(len(t))]


def right(t):
    return [t[i][-1] for i in range(len(t))]


def sides(t):
    # clockwise from top
    return [top(t), right(t), bot(t), left(t)]


def sides8(tile):
    normals = sides(tile)
    flipped = [i[::-1] for i in sides(tile)]
    my_sides = normals + flipped
    return my_sides


test = tiles[1847]

# can be flipped or rotated
# 8 orientations per tile
# edges line up exactly
# reversing an edge to see if same is a start
# 8 `sides` per tile each one flipped
# top,right,bottom,left, reversed(top,right,bottom,left)

idxside = {0: "t", 1: "r", 2: "b", 3: "l", 4: "tr", 5: "rr", 6: "br", 7: "lr"}

all_sides = dict()
for _id, tile in tiles.items():
    # for i,s in E(my_sides):
    #     print(i, s)
    all_sides[_id] = sides8(tile)

touching = dict()
shared_sides = dict()
for o_id, o_tile in tiles.items():
    # try to find matching sides somewhere
    # matching side = (id, idx)
    matching_sides = [[] for _ in range(8)]  # per self-idx
    my_sides = sides8(o_tile)
    for i_id, i_sides in all_sides.items():
        if i_id == o_id:
            continue
        for my_idx, my_side in enumerate(my_sides):
            for their_idx, their_side in enumerate(i_sides):
                if their_side == my_side:
                    them = (i_id, their_idx)
                    matching_sides[my_idx].append(them)
                    already_touching = touching.get(o_id, set())
                    already_touching.add(i_id)
                    touching[o_id] = already_touching
    shared_sides[o_id] = matching_sides

# for k, v in shared_sides.items():
#     print([len(i) for i in v])

# every side has only one that it can pair up with
print("corners found, only two shared sides")
tot = 1
for k, v in touching.items():
    if len(v) == 2:
        print(k, shared_sides[k])
        tot *= k
# not 25012634094023 (too high)
ans(tot)  # 21599955909991

# now actually find indexes, rotations for each tile
"""corners:
2521 
2633 
3067 
1061 
"""
positions = dict()
# assume 3067 is top left, whatever
# 12 x 12 box i suppose
# which index is on top?
# x, y, r
# |  |  |
# |  |  Rotation
# |  position
# position


def show(t, spacing = ' ',monsters=set()):
    out = ""
    s = spacing
    for y in range(len(t)):
        for x in range(len(t[y])):
            cur = t[y][x]
            if (x, y) in monsters:
                out += "O" + s
            elif cur is True:
                out += "#" + s
            elif cur is False:
                out += "." + s
            else:
                out += str(cur)[0] + s
        out += "\n"
    out = out[:-1]
    print(out)


def show2(t, monsters = set()):
    # with spaces between lines and columns
    out = ""
    width = len(t[0])
    posts = width // 12
    hoz_line = " " * (width + posts + 1)
    for y in range(len(t)):
        for x in range(len(t[y])):
            cur = t[y][x]
            if (x, y) in monsters:
                out += "O"
            elif cur is True:
                out += "#"
            elif cur is False:
                out += "."
            else:
                out += str(cur)[0]
            if ((x+1) % posts)  == 0:
                out += " "
        if ((y+1) % posts)  == 0:
            out += "\n" + hoz_line + "\n"
        else:
            out += "\n"
    print(out)


def rotate(t):
    # rotate counter_clockwise once
    nu = deepcopy(t)
    return list(zip(*nu))[::-1]


def hoz_flip(t):
    nu = deepcopy(t)
    return [l[::-1] for l in nu]


def eq(r1, r2):
    z = zip(r1, r2)
    return all([a == b for a, b in z])


def orientations(t):
    nu = deepcopy(t)
    ors = []
    for _ in range(4):
        ors.append(nu)
        nu = rotate(nu)
    nu = hoz_flip(nu)
    for _ in range(4):
        ors.append(nu)
        nu = rotate(nu)
    return ors


# dicts: touching, tiles, shared_sides, all_sides
TOPRIGHT = 3067
positions[3067] = (11, 0, 0)
coordinates = dict()
coordinates[(11, 0)] = (3067, 0)


def place_below(anchor_id, flipper_id):
    anchor = deepcopy(tiles[anchor_id])
    flipper = deepcopy(tiles[flipper_id])
    ankx, anky, ankrot = positions[anchor_id]
    anchor = orientations(anchor)[ankrot]  # rotate anchor to its orientation
    flipps = orientations(flipper)
    for fliprot, flipp in E(flipps):
        if eq(top(flipp), bot(anchor)):
            putme = (ankx, anky + 1, fliprot)
            positions[flipper_id] = (ankx, anky + 1, fliprot)
            coordinates[(ankx, anky + 1)] = (flipper_id, fliprot)
            return flipper_id, putme
    return False


def place_left(anchor_id, flipper_id):
    anchor = deepcopy(tiles[anchor_id])
    flipper = deepcopy(tiles[flipper_id])
    ankx, anky, ankrot = positions[anchor_id]
    anchor = orientations(anchor)[ankrot]  # rotate anchor to its orientation
    flipps = orientations(flipper)
    for fliprot, flipp in E(flipps):
        if eq(right(flipp), left(anchor)):
            putme = (ankx, anky + 1, fliprot)
            positions[flipper_id] = (ankx - 1, anky, fliprot)
            coordinates[(ankx - 1, anky)] = (flipper_id, fliprot)
            return flipper_id, putme
    return False


cur_anchor = TOPRIGHT


curx = 11
cury = 0

x_idx = 11
while x_idx > 0:
    for t in touching[cur_anchor]:
        worked = place_left(cur_anchor, t)
        if worked:
            x_idx -= 1
            cur_anchor = worked[0]
            break

# top row is filled

for x_offset in range(12)[::-1]:
    y_idx = 0
    cur_anchor = coordinates[(x_offset, y_idx)][0]  # just id
    while y_idx < 11:
        for t in touching[cur_anchor]:
            worked = place_below(cur_anchor, t)
            if worked:
                y_idx += 1
                cur_anchor = worked[0]
                break

print(coordinates)
# coordinates filled in by id
for y in range(12):
    for x in range(2, 3):
        key, rot = coordinates[(x, y)]
        shape = orientations(tiles[key])[rot]
        # print("-"*24)
        # show(shape)

print("corners and their orientations: ")
for c in ((0, 0), (11, 0), (11, 11), (0, 11)):
    print(coordinates[c])


def show_coord(c):
    tile_id, rotidx = coordinates[c]
    show(orientations(tiles[tile_id])[rotidx])


def shrink(tile):
    # turn tile into a smaller version of itself
    nu_tile = deepcopy(tile)
    shrunk = [line[1:-1] for line in nu_tile[1:-1]]
    return shrunk


test = [[i for i in range(6)] for _ in range(6)]

big_coords = dict()
bigy = 0
bigx = 0
for y in range(12):
    for x in range(12):
        tile_id, rotidx = coordinates[(x, y)]
        cur = deepcopy(tiles[tile_id])
        cur = orientations(cur)[rotidx]
        # show(cur)
        cur = shrink(cur)
        dimy = len(cur)
        dimx = len(cur[0])
        for yy in range(len(cur)):
            for xx in range(len(cur[yy])):
                val = cur[yy][xx]  # true or false
                xxx = x * dimx + xx
                yyy = y * dimy + yy
                if yyy > bigy:
                    bigy = yyy
                if xxx > bigx:
                    bigx = xxx
                big_coords[(xxx, yyy)] = val

# we now have T/F on a big grid with all the shrinking and rotations applied
# grid is 8x8 x 12x12 = 9216 squares
big_tile = []
for y in range(bigy + 1):
    cur_line = [big_coords[(x, y)] for x in range(bigx + 1)]
    big_tile.append(cur_line)

# show2(big_tile)
# exit()
sea_monster = """\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""
sl = sea_monster.splitlines()
print(sl)
monster_positions = []
for y in range(len(sl)):
    for x in range(len(sl[y])):
        if sl[y][x] == "#":
            monster_positions.append((x, y))

max_monster_count = 0
for idx, sea in E(orientations(big_tile)):
    coord_is_monster = set()
    monster_count = 0
    for ybox in range(len(sea)):
        for xbox in range(len(sea[ybox])):
            try:
                check_coords = [(x + xbox, y + ybox) for x, y in monster_positions]
                ismon = all([sea[yy][xx] == True for xx, yy in check_coords])
                if ismon:
                    for c in check_coords:
                        if c in coord_is_monster:
                            print("ALREATDDY")
                        coord_is_monster.add(c)
                    print('monster at: ', xbox, ybox)
                    monster_count += 1
                    if monster_count > max_monster_count:
                        max_monster_count = monster_count
            except:
                pass
    if monster_count:
        print(f"{monster_count} monsters at sea[{idx}]")
        # show(sea, spacing='', monsters=coord_is_monster)
        break
tot = 0
for y in range(len(big_tile)):
    for x in range(len(big_tile[y])):
        if big_tile[y][x] == True:
            tot += 1
tot -= max_monster_count * len(monster_positions)
ans(tot)  # 2495
# not 2719 (too high)
