"""
I am almost sure there's an off by one in this program
or an unchecked range, but I found answers nonetheless
"""

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

print(lines)
print(len(lines), "lines in input.txt")


def ans(answer):
    # store answer to clipboard
    print(answer, "| in clipboard")
    os.system(f'echo "{answer}"| xclip -selection clipboard -in')


def line_transform(line):
    # split = [line.split() for line in lines]
    return int(line)


line_groups = data.split("\n\n")  # lines split by double newlines
lines = [line_transform(line) for line in lines]  # apply line_transform to each line

L, I, D, S = list, int, dict, set
P, E, R, M = print, enumerate, range, map
## end of boilerplate


def check25(lines):
    goal = lines[-1]
    for ai, a in enumerate(lines):
        for bi, b in enumerate(lines):
            if a + b == goal and ai != bi:
                return True
    ans(goal)  # 25918798
    return False


offset = 26
while offset < len(lines) - 1:
    sl = lines[offset - 26 : offset]
    if not check25(sl):
        print(sl)
    offset += 1


goalie = 25918798

start = 0
end = 0
while True:
    sl = lines[start : end + 1]
    s = sum(sl)
    if s == goalie:
        print(sl)
        ans(max(sl) + min(sl))  # 3340942
        exit()
    if s > goalie:
        start += 1
        end = start
        continue
    end += 1
