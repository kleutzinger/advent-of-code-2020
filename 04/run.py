lines = []
with open("input.txt") as f:
    lines = [x.strip().split(" ") for x in f.readlines()]
print(lines)
print(len(lines), "lines in input.txt")
# split = [line.split() for line in lines]
# print(split)

"""
byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)
"""
required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
ports = [[]]
seen = dict()
for l in lines:
    things = [l.split(":") for l]
    for thing in things:
        seen[thing] = True
    if l == "\n":
        seen = dict()
    if all([i in required for i in seen.keys()]):
        print("true")

print(ports)
