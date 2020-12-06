with open("input.txt") as f:
    data = f.read()
    lines = data.splitlines()
print(lines)
print(len(lines), "lines in input.txt")


def line_transform(line):
    split = [line.split() for line in lines]
    return line


line_groups = line.split("\n\n")
lines = [line_transform(line) for line in lines]

## end of boilerplate