import os

# change to dir of script
os.chdir(os.path.dirname(__file__))

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
    return line


line_groups = data.split("\n\n")  # lines split by double newlines
lines = [line_transform(line) for line in lines]  # apply line_transform to each line

L, I, D = list, int, dict
P, M = print, map
S, J = str.split, str.join
## end of boilerplate
