lines = []
with open("input.txt") as f:
    # lines = [x.strip() for x in f.readlines()]
    lines = f.read()
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


passports = lines.split("\n\n")
print(passports)
required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

valid = 0
for p in passports:
    if all([r in p for r in required]):
        valid += 1

print(valid)

## 2
"""
byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
If cm, the number must be at least 150 and at most 193.
If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid(Country ID) - ignored, missing or not.
"""

import re


def valid_height(s):
    try:
        pass
        unit = s[-2:]
        num = int(s[:-2])
        if unit not in ["in", "cm"]:
            return False
        if unit == "cm":
            return num >= 150 and num <= 193
        else:
            return num >= 59 and num <= 76
    except:
        return False


prog = re.compile(r"^#[0-9a-f]{6}$")
pid = re.compile(r"^[0-9]{9}$")
req_validators = [
    lambda x: int(x) >= 1920 and int(x) <= 2002,
    lambda x: int(x) >= 2010 and int(x) <= 2020,
    lambda x: int(x) >= 2020 and int(x) <= 2030,
    valid_height,
    lambda x: bool(prog.match(x)),
    lambda x: x in "amb blu brn gry grn hzl oth".split(" "),
    lambda x: bool(pid.match(x)),
]


def get_value(p, f):
    for i, col_split in enumerate(p.split(":")):
        print(col_split)
        if col_split[0] == f:
            return p.split(":")[i + 1].split(" ")[0]
    return ""


def find_and_validate_all(p):
    validators = zip(required, req_validators)
    for idx in range(7):
        try:
            key = required[idx]
            validator = req_validators[idx]
            val = get_value(p, key)
            print(val)
            if not validator(get_value(p, key)):
                print("bad")
                return False
        except:
            print("except")
            return False
    print("good")
    return True


valid = 0
for p in passports:
    if find_and_validate_all(p):
        valid += 1

print(valid)  ## INCOMPLETE pt 2
