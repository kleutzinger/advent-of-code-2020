lines = []
with open("input.txt") as f:
    lines = [x.strip() * 100 for x in f.readlines()]
# print(lines)

width = len(lines[0])
height = len(lines)
x = 0
y = 0
dx = 3
dy = 1


def find_tree_count(ds):
    x = 0
    y = 0
    dx = ds[0]
    dy = ds[1]
    tree_cnt = 0
    while x < width - 1 and y < height - 1:
        x += dx
        y += dy
        # print(x, y)
        if lines[y][x] == "#":
            tree_cnt += 1
            # print("tree")
        else:
            pass
            # print("notree")
    # print(width, height)
    print(tree_cnt)
    return tree_cnt


tot = 1

for dd in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
    tot = tot * find_tree_count(dd)
    print(tot)

print(tot)