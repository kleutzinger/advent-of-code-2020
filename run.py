lines = []
with open("input.txt") as f:
    lines = [x.strip() for x in f.readlines()]
print(lines)
print(len(lines), "lines in input.txt")
# split = [line.split() for line in lines]
# print(split)
