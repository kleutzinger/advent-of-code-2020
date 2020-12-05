lines = []
with open("input.txt") as f:
    data = f.read()
    lines = data.splitlines()
print(lines)
print(len(lines), "lines in input.txt")
# split = [line.split() for line in lines]
# print(split)


def get_row(s):
    s = s[:7]
    s = s.replace("F", "0")
    s = s.replace("B", "1")
    return int(s, 2)


def get_column(s):
    s = s[-3:]
    s = s.replace("L", "0")
    s = s.replace("R", "1")
    return int(s, 2)


def get_id(line):
    row = get_row(line)
    column = get_column(line)
    return row * 8 + column


ids = [get_id(s) for s in lines]
print(max(ids))

## pt 2

sort = list(sorted(ids))
print(sort)
diff = 1
for idx, id in enumerate(sort):
    diff = id - sort[idx + 1]
    if diff != -1:
        print(id)
        break
# above is actually an off by one, it prints 618,
# but i verified in the print on line 37 the actual
# missing id value (619)

## bonus work ##

# find missing seat number
rg = range(min(ids), max(ids))
print(set(rg) - set(ids))  # {619}
