from python_utils.zac_pyutils import ExqUtils
from python_utils.zac_pyutils import ExqLog
from python_utils.zac_pyutils.ExqUtils import zprint
import time
import random
import itertools


def test_zprint():
    zprint("abc", "efd", "gear")


def test_logger():
    logger = ExqLog.get_file_logger(info_log_file="info.log", err_log_file="err.log")
    logger.debug("a debug")
    logger.info("a info")
    logger.error("a error")


def test_groupby():
    item = [(1, 2, 'a'), (1, 3, 'b'), (1, 4, 'c'), (2, 2, 'd'), (2, 3, 'e'), (2, 4, 'f')]
    random.shuffle(item)
    item2 = [1, 2, 3, 4, 5, 1, 1, 1, 6, 2, 2, 2, 7, 7, 7, 5, 4, 4, 3, 6, 8, 8]

    zprint("ExqUtils default:")
    for k, g in ExqUtils.groupby(item2):
        print(k, list(g))
    zprint("ExqUtils:")
    for k, g in ExqUtils.groupby(item, key=lambda x: x[1]):
        print(k, list(g))
    zprint("itertools:")
    for k, g in itertools.groupby(item, key=lambda x: x[1]):
        print(k, list(g))


def test_map_on_iter():
    item = range(0, 5000, 7)
    print("iterItem is ", list(item))
    res = ExqUtils.map_on_iter(iter(item), lambda item_iter: map(lambda it: it - 10, item_iter), 10)
    print(res)


def test_time_it():
    @ExqUtils.timeit
    def time_test(run_time, b):
        print("sleep for {} sec".format(run_time))
        time.sleep(run_time)
        print(b)
        print("done.")
        return "time_test's return"

    print(time_test(3, "someone"))
    print(time_test(5, "another"))


if __name__ == '__main__':
    # 验证zprint
    test_zprint()

    # 验证logger
    test_logger()

    # 验证 groupby
    test_groupby()

    # 验证 map_on_iter 方法
    test_map_on_iter()

    # 验证 timeit
    test_time_it()
