lines = []
with open("input.txt") as f:
    lines = [x.strip() for x in f.readlines()]
print(lines)

split = [line.split() for line in lines]
print(split)

valid_count = 0
for entry in split:
    rg = entry[0].split("-")
    rg = range(int(rg[0]), int(rg[1]) + 1)
    char = entry[1][0]
    if entry[2].count(char) in rg:
        valid_count += 1

print(valid_count, len(split))  # 620 1000
# part 2

valid_count = 0
for entry in split:
    # print(entry)
    rg = entry[0].split("-")
    idx1 = int(rg[0]) - 1
    idx2 = int(rg[1]) - 1
    char = entry[1][0]
    total = 0
    try:
        if entry[2][idx1] == char:
            total += 1
    except:
        pass
    try:
        if entry[2][idx2] == char:
            total += 1
    except:
        pass
    if total == 1:
        valid_count += 1
print(valid_count)  # 727

# ~ 15 min total