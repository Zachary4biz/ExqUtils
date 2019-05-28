from python_utils.zac_pyutils import ExqUtils

if __name__ == '__main__':
    ExqUtils.zprint("abc")

    item = range(0, 50, 7)
    print("iterItem is ", list(item))
    res = ExqUtils.map_on_iter(iter(item), lambda it: map(lambda item: item - 10, it), 10)
    print([list(i) for i in res])
