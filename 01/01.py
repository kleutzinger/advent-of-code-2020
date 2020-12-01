nums = []
with open("input.txt") as f:
    nums = [int(x.strip()) for x in f.readlines()]

print(nums)

for a in nums:
    for b in nums:
        if a + b == 2020:
            print(a, b, a * b)
            # 279 1741 485739
            # 1741 279 485739

# part2
for a in nums:
    for b in nums:
        for c in nums:
            if a + b + c == 2020:
                print(a, b, c, a * b * c)
                # 1269 257 494 161109702
