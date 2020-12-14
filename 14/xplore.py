def string_gen(xin, opts):
    # replace instances of X in xin with any of [opts]
    # return the list of all possible substiutions applied
    # base case: no X left, return xin
    # recursive case:
    #   call generate xin with from each option
    # this `works`, but it returns a list nested by how many X's in xin
    x_idx = xin.find("X")
    if x_idx == -1:
        # results.append(xin)
        print(xin)
        return xin
    else:
        left, _, right = xin.partition("X")
        # how do I get this to not become nested?
        return [string_gen(left + o + right, opts) for o in opts]


i = "AXXB"
o = ["0", "1", "two"]
print(string_gen(i, o))
"""
[
    ['A00B', 'A01B', 'A0twoB'],
    ['A10B', 'A11B', 'A1twoB'], 
    ['Atwo0B', 'Atwo1B', 'AtwotwoB']
]

Is there a way to use yield to do this?
"""
