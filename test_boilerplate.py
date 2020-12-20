import boilerplate as bp


def test_ps():
    inp = [0, 1]
    assert list(bp.powerset(inp)) == [(), (0,), (1,), (0, 1)]


def test_coords():
    inp = [[0, 0, 0], [0], [0, 0, 0, 0]]
    out = [inp[y][x] for x, y in bp.coords(inp)]
    out = [i == 0 for i in out]
    assert all(out)


def test_commaints():
    inp = "0,1, 2 ,   3"
    out = bp.comma_ints(inp)
    assert out == [0, 1, 2, 3]
