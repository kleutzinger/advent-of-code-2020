import os

# change to dir of script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt") as f:
    data = f.read()  # entire file as string
    lines = data.splitlines()
print(lines)
print(len(lines), "lines in input.txt")


def ans(answer):
    # store answer to clipboard
    print(answer, "| in clipboard")
    os.system(f'echo "{answer}" | xsel --clipboard')


def line_transform(line):
    # split = [line.split() for line in lines]
    parent = line.split(" bags")[0]
    children = line.split("contain")[1].split(",")
    children = list(map(str.strip, children))
    children = [" ".join(child.split(" ")[1:-1]) for child in children]
    if children == ["other"]:
        return [parent, []]
    return [parent, children]


line_groups = data.split("\n\n")  # lines split by double newlines
lines = [line_transform(line) for line in lines]  # apply line_transform to each line

## end of boilerplate

print(lines)

tree = dict()
for parent, children in lines:
    tree[parent] = children


def traverse1(parent):
    children = tree[parent]
    if "shiny gold" in children:
        print(parent)
        return True
    else:
        return any([traverse1(child) for child in children])


tot = 0
for p in tree:
    if traverse1(p):
        tot += 1

ans(tot)  # 370  # part 1


def line_transform2(line):
    # split = [line.split() for line in lines]
    parent = line.split(" bags")[0]
    children = line.split("contain")[1].split(",")
    children = list(map(str.strip, children))
    if children[0].startswith("no other"):
        return (parent, {})
    amounts = [int(c.split(" ")[0]) for c in children]
    names = [" ".join(c.split(" ")[1:-1]) for c in children]
    return [parent, dict(zip(names, amounts))]


tree = dict()
for parent, children in list(map(line_transform2, data.splitlines())):
    tree[parent] = children


def inside(parent_name, so_far):
    print(parent_name)
    if tree[parent_name] == {}:
        print("no children in " + parent_name)
        return so_far
    else:
        print(tree[parent_name].items())
        return sum(tree[parent_name].values()) + sum(
            [
                amount * inside(name, so_far)
                for name, amount in tree[parent_name].items()
            ]
        )


# total = 0
# for child, value in tree["shiny gold"].items():
#     print(child, value)

ans(inside("shiny gold", 0))  # 29547 part 2

# base case:
# children == {}:
#   return running total
# 1 * muted olive children +
# 5 * dotted red children +
# 1 * drab plum children
print(tree["shiny gold"])

# about 1.5 hours