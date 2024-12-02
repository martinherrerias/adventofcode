import re

line = "?#?????1???#??? 3,1,3,2"
print(line)
print("".join(list(map(str, range(9)))))

groups = re.findall(r"\d+", line)

gpat = lambda g: f"(?<!#)([#?]{{{g}}})(?!#)"

ggpat = lambda gg: "[^#]+".join([gpat(g) for g in gg])


def test_from(g0, c0):

    print(f"test from g {g0+1}, c {c0}")

    if c0 > len(line) - 1:
        ok = g0 > len(groups) - 1
        n = int(ok)
        print(f"end od line, {n} ways")
        return n

    if g0 > len(groups) - 1:
        ok = re.match("[^#]*", line[c0:]) is not None
        n = int(ok)
        print(f"end of groups, {n} ways")
        return n

    gg = groups[g0:]
    P = ggpat(gg)
    p = gpat(groups[g0])

    n = 0
    for i in range(c0, len(line)):
        if line[i] == ".":
            continue
        if i > 0 and line[i - 1] == "#":
            break

        if not re.match(P, line[i:]):
            continue
        m = re.match(p, line[i:])
        print(f"g {gg} match at {i}")
        n += test_from(g0 + 1, i + len(m.groups(1)[0]) + 1)

    print(f"{n} ways")
    return n


test_from(0, 0)
