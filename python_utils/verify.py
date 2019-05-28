from python_utils.zac_pyutils import ExqUtils

if __name__ == '__main__':
    ExqUtils.zprint("abc")

    item = range(0, 5000, 7)
    print("iterItem is ", list(item))
    res = ExqUtils.map_on_iter(iter(item), lambda item_iter: map(lambda it: it - 10, item_iter), 10)
    print(res)
