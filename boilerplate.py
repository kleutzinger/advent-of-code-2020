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


L, I, D, S = list, int, dict, set
P, E, R, M = print, enumerate, range, map
## end of boilerplate


def line_transform(line):
    # split = [line.split() for line in lines]
    # ints = [int(line) for line in lines]
    return line


line_groups = data.split("\n\n")  # lines split by double newlines
lines = [line_transform(line) for line in lines]  # apply line_transform to each line
