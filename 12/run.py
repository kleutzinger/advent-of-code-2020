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


def line_transform(line):
    # split = [line.split() for line in lines]
    # return int(line)
    d = line[0]
    mag = int(line[1:])
    return d, mag


lines = [line_transform(line) for line in lines]  # apply line_transform to each line

ship = [0, 0]
facing = 0

dist = lambda s: abs(s[0]) + abs(s[1])

for d, mag in lines:
    print(d, mag)
    dx, dy = 0, 0
    if d == "N":
        dy = -1 * mag
    if d == "S":
        dy = 1 * mag
    if d == "W":
        dx = -1 * mag
    if d == "E":
        dx = 1 * mag
    if d == "L":
        facing += mag
    if d == "R":
        facing -= mag
    facing = facing % 360
    if d == "F":
        if facing == 0:
            dx = mag
        if facing == 90:
            dy = -mag
        if facing == 180:
            dx = -mag
        if facing == 270:
            dy = mag
    ship[0] += dx
    ship[1] += dy
    print(ship, facing)

ans(dist(ship))  # 1186

## part 2

ship = [0, 0]
facing = 0
waypoint = [10, -1]


def rot(ship, way, deg):
    # move ship to origin, rotate waypoint clockwise(?)
    shipoff = -ship[0], -ship[1]
    way[0] += shipoff[0]
    way[1] += shipoff[1]
    while deg > 0:
        way[0], way[1] = -way[1], way[0]
        deg -= 90
    way[0] -= shipoff[0]
    way[1] -= shipoff[1]
    return way


for d, mag in lines:
    print(d, mag)
    dx, dy = 0, 0
    wdx, wdy = 0, 0
    if d == "N":
        wdy = -1 * mag
    if d == "S":
        wdy = 1 * mag
    if d == "W":
        wdx = -1 * mag
    if d == "E":
        wdx = 1 * mag
    if d == "R":
        waypoint = rot(ship, waypoint, mag)
    if d == "L":
        waypoint = rot(ship, waypoint, 360 - mag)
    if d == "F":
        difx = waypoint[0] - ship[0]
        dify = waypoint[1] - ship[1]
        wdx, wdy = mag * difx, mag * dify
        dx, dy = mag * difx, mag * dify
    waypoint[0] += wdx
    waypoint[1] += wdy
    ship[0] += dx
    ship[1] += dy
    # print(ship, facing)
    print(waypoint)

ans(dist(ship))  # 47806
