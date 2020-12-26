header = """\
      ----Part 1----    ----Part 2----
Day       Time  Rank       Time   Rank  """

data = """
 25   00:19:37  1423   05:07:59   5105
 24   00:22:15  1249   00:47:28   1309
 23   00:47:30  1968       >24h  11024
 22   00:09:52  1059   03:11:45   4095
 21   00:43:58  1777   00:47:58   1424
 20   01:16:05  1801   05:18:06   1561
 19   01:27:58  2552   04:13:11   3089
 18   01:43:05  4634   01:54:37   3606
 17   00:34:47  1402   02:00:06   3918
 16   00:15:50  1280   01:30:48   3256
 15   01:10:49  6162   01:22:33   5138
 14   00:26:58  2467   01:18:30   3282
 13   00:20:49  4479   03:41:06   5069
 12   00:11:06  1004   00:28:35   1437
 11   00:55:57  4828   01:29:44   4497
 10   00:13:22  3736   02:45:43   7487
  9   00:09:27  1934   00:16:24   1554
  8   00:07:57  1475   00:18:22   1377
  7   00:26:46  2018   01:27:52   4915
  6   00:05:45  1479   00:11:27   1513
  5   00:09:32  1116   00:12:32    864
  4   00:26:57  5359       >24h  73891
  3   00:07:21  1435   00:12:00   1341
  2   00:07:21  1461   00:15:15   2114
  1   00:50:59  5530   00:52:35   5010"""

part1 = []  # [ (time, rank), ...]
part2 = []
for line in data.splitlines()[::-1]:
    if line == "":
        continue
    columns = line.split(" ")
    columns = filter(lambda c: c != "", columns)
    columns = list(columns)
    day, time1, rank1, time2, rank2 = columns
    part1.append({"day": day, "part": 1, "time": time1, "rank": rank1})
    part2.append({"day": day, "part": 2, "time": time2, "rank": rank2})


def median(seq, key=lambda x: x):
    ordered = sorted(seq, key=key)
    size = len(seq)
    if size % 2 == 1:
        return ordered[len(seq) // 2]
    if size % 2 == 0:
        a = ordered[size // 2]
        b = ordered[size // 2 - 1]
        avg = (key(a) + key(b)) / 2
        return avg


def best(seq, key=lambda x: x):
    return sorted(seq, key=key)[0]


def hms_to_sec(t):
    if t == ">24h":
        return 99999999
    mult = 1
    seconds = 0
    t = t.split(":")
    while len(t):
        seconds += int(t.pop()) * mult
        mult *= 60
    return seconds


def col_gen(part, aggr, key_str):
    if key_str == "time":
        key = lambda p: hms_to_sec(p["time"])
    if key_str == "rank":
        key = lambda p: int(p["rank"])
    ans_obj = aggr(part, key=key)
    day = ans_obj["day"]
    val = ans_obj[key_str]
    if aggr != median:
        out = f"{val} (day {day})"
    else:
        out = f"{val}"
    return out


m_time1 = col_gen(part1, median, "time")
m_rank1 = col_gen(part1, median, "rank")

m_time2 = col_gen(part2, median, "time")
m_rank2 = col_gen(part2, median, "rank")


b_time1 = col_gen(part1, best, "time")
b_rank1 = col_gen(part1, best, "rank")


b_time2 = col_gen(part2, best, "time")
b_rank2 = col_gen(part2, best, "rank")

# print(f'```{data}\n```')

md = f"""\
Part   | Median Time | Median Rank  | Fastest Time| Best Rank
-------| ------------| -------------|-------------|----------
Part 1 | {m_time1}   | {m_rank1}    | {b_time1}   | {b_rank1}
Part 2 | {m_time2}   | {m_rank2}    | {b_time2}   | {b_rank2}
"""

with open('stats.md', 'w') as f:
    out = f"```\n{header}\n{data}\n```\n\n{md}\n"
    print(out, file=f)
