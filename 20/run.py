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

tiles = dict()
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

# get borders of a tile
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
    # get all 8 possible borders
    # 4 sides * 2 (unflipped|flipped)
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

all_sides = dict()
for _id, tile in tiles.items():
    # for i,s in E(my_sides):
    #     print(i, s)
    all_sides[_id] = sides8(tile)

touching = dict()
shared_sides = dict()
# touching: find tile_ids that touch each other
# shared_sides: find sides per-tile that are compatible with another tile's side
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

for k, v in shared_sides.items():
    pass
    # print([i for i in v])

# every side has one or zero sides that it can pair up with
print("corners found, only two shared sides")
tot = 1
for k, v in touching.items():
    if len(v) == 2:
        print(str(k) + ":", shared_sides[k])
        tot *= k
# not 25012634094023 (too high)
ans(tot)  # 21599955909991

## part 2 ##

# now actually find indexes, rotations for each tile
"""corners:
2521 2633 3067 1061 
"""
# assume 3067? is top right, whatever
# 12 x 12 box i suppose
# which index is on top?
# x, y, r
# |  |  |
# |  |  Rotation
# |  position
# position


def show(t, spacing=" ", monsters=set()):
    # print out a tile
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


def show2(t, monsters=set()):
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
            if ((x + 1) % posts) == 0:
                out += " "
        if ((y + 1) % posts) == 0:
            out += "\n" + hoz_line + "\n"
        else:
            out += "\n"
    print(out)


def rotate(t):
    # rotate a tile counter_clockwise once
    nu = deepcopy(t)
    return list(zip(*nu))[::-1]


def hoz_flip(t):
    # reverse a tile left to right
    nu = deepcopy(t)
    return [l[::-1] for l in nu]


def eq(r1, r2):
    # check if r1's contents == r2's contents
    # can do eq(tuple, list)
    z = zip(r1, r2)
    return all([a == b for a, b in z])


def orientations(t):
    # return a list of the tile re-worked into 8 possible orientations
    # [rot0, rot1, rot2, rot3] + hoz_flip([rot0, rot1, rot2, rot3])
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


def place_below(anchor_id, flipper_id):
    # anchor is an oriented, positioned tile on the grid
    # flipper is a tile we attempt to orient and place below the anchor
    # we know which 2-4 tiles touch the anchor, and each has 8 orientations
    # but only one tile+orientation can attatch to the bottom
    # if flipper has no viable top for anchors bottom, return False
    # else return flipper_id, (fx, fy, frot)
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
    # same as above, but placing to the left
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


# dicts: touching, tiles, shared_sides, all_sides
positions = dict()
# positions = {tile_id -> ( coord_x, coord_y, rotation_index(0-8) )}
# map tile id to
coordinates = dict()
# coordinates = { (x,y) -> ( tile_id, rotation_index ) }

# hardcode and place a top right value
# chose this one because it does not require any pre-rotation
TOPRIGHT_ID = 3067
positions[TOPRIGHT_ID] = (11, 0, 0)
coordinates[(11, 0)] = (TOPRIGHT_ID, 0)

# move anchor along the top, filling in all positions to the left
# cur_anchor is a tile_id from where we attempt to attatch `flippers`
# flippers are chosen from the cur_anchor's `touching` dict items
cur_anchor = TOPRIGHT_ID
x_idx = 11
while x_idx > 0:
    for t in touching[cur_anchor]:
        worked = place_left(cur_anchor, t)
        if worked:
            # set new anchor to just-placed tile, and move left
            x_idx -= 1
            cur_anchor = worked[0]
            break

# top row is filled with tiles
# fill in each column going down from the top
# go down columns right to left
for x_offset in range(12)[::-1]:
    # move left to next column
    y_idx = 0
    cur_anchor = coordinates[(x_offset, y_idx)][0]  # just id
    while y_idx < 11:
        for t in touching[cur_anchor]:
            worked = place_below(cur_anchor, t)
            if worked:
                # set new anchor to just-placed tile, and move down
                y_idx += 1
                cur_anchor = worked[0]
                break
# each coordinate now has a tile_id and an orientation associated with it
print(coordinates)

print("corners and their orientations: ")
for c in ((0, 0), (11, 0), (11, 11), (0, 11)):
    print(coordinates[c])


def show_coord(c):
    # show an oriented tile at a given coordinate
    tile_id, rotidx = coordinates[c]
    show(orientations(tiles[tile_id])[rotidx])


def shrink(tile):
    # turn tile into a smaller version of itself
    # remove the borders
    nu_tile = deepcopy(tile)
    shrunk = [line[1:-1] for line in nu_tile[1:-1]]
    return shrunk


# run through positioned tiles and set coordinates on a big, global tile
big_coords = dict()
maxy = 0
maxx = 0
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
                if yyy > maxy:
                    maxy = yyy
                if xxx > maxx:
                    maxx = xxx
                big_coords[(xxx, yyy)] = val

# we now have T/F on a big grid with all the shrinking and rotations applied
# grid is 8x8 x 12x12 = 9216 squares
big_tile = []
for y in range(maxy + 1):
    cur_line = [big_coords[(x, y)] for x in range(maxy + 1)]
    big_tile.append(cur_line)

# show2(big_tile)
# exit()
sea_monster = """\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""
print(sea_monster)
sl = sea_monster.splitlines()
monster_positions = []
for y in range(len(sl)):
    for x in range(len(sl[y])):
        if sl[y][x] == "#":
            monster_positions.append((x, y))

# we have eight sea orientations, let's find our monsters in them
max_monster_count = 0
for idx, sea in E(orientations(big_tile)):
    coord_is_monster = set()
    monster_count = 0
    height_rg = range(len(sea))
    width_rg = range(len(sea[0]))
    # xbox, ybox define the top left corner for a candidate monster-shape
    for ybox in height_rg:
        for xbox in width_rg:
            # check these coords in sea to see if all active ("a monster")
            check_coords = [(x + xbox, y + ybox) for x, y in monster_positions]
            inbounds = all(
                [yy in height_rg and xx in width_rg for xx, yy in check_coords]
            )
            if not inbounds:
                continue
            ismon = all([sea[yy][xx] == True for xx, yy in check_coords])
            if ismon:
                # we found a moenster
                for c in check_coords:
                    if c in coord_is_monster:
                        print("Monster collision at ", c)
                        assert False, c
                    coord_is_monster.add(c)
                print("monster at: ", xbox, ybox)
                monster_count += 1
                if monster_count > max_monster_count:
                    max_monster_count = monster_count
    if monster_count:
        # only one sea has any monsters in it. end search if found
        print(f"{monster_count} monsters at sea[{idx}]")
        # show(sea, spacing='', monsters=coord_is_monster)
        break
tot = 0
# count active tiles
for y in range(len(big_tile)):
    for x in range(len(big_tile[y])):
        if big_tile[y][x] == True:
            tot += 1
# remove monster-tiles from count
tot -= max_monster_count * len(monster_positions)
ans(tot)  # 2495
# not 2719 (too high)
