# encoding:utf-8
from python_utils.zac_pyutils import ExqUtils
from python_utils.zac_pyutils import ExqLog
from python_utils.zac_pyutils.Timeout import TimeoutThread,TimeoutProcess
from python_utils.zac_pyutils.ExqUtils import zprint
import time
import random
import itertools


def test_zprint():
    zprint("验证zprint支持输入多个字符串作为参数：自动空格连接", "参数2", "参数3")


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
        for i in range(run_time):
            time.sleep(1)
            print(i)
        print("input b is: {}".format(b))
        return "time_test finished after runtime: {}".format(run_time)

    print(time_test(3, "someone"))
    print(time_test(5, "another"))


def test_timeout():
    def target_func(inp, timeout=5):
        print("子线程预计执行 {}秒".format(timeout))
        for i in range(timeout):
            time.sleep(1)
            print("子线程执行中：{}".format(i))
        print("输入参数inp最后增加100")
        return inp + 100

    zprint("case1： 超时时间为8秒，子线程运行耗时3秒， 预计三秒后子线程结束、主线程不再被block")
    t1 = TimeoutThread(target=target_func, args=(30,3), time_limit=8)
    result = t1.start()
    zprint("参数结果是 {}".format(result))

    zprint("case1： 超时时间为3秒，子线程运行耗时8秒， 预计三秒后主线程不再block，子线程被强制结束")
    t2 = TimeoutThread(target=target_func, args=(30, 8), time_limit=3)
    res2 = t2.start()
    zprint("参数结果是 {}".format(res2))
    time.sleep(9)

def test_timeout_process():
    def target_func(inp, timeout=5):
        print("    [target_func]: 子线程预计执行 {}秒".format(timeout))
        for i in range(timeout):
            time.sleep(1)
            print("    [target_func]: 子线程执行中：{}".format(i))
        print("    [target_func]: 输入参数inp最后增加100")
        return inp + 100

    def taget_no_return(inp, timeout=5):
        print("    [target_func]: 子线程预计执行 {}秒".format(timeout))
        for i in range(timeout):
            time.sleep(1)
            print("    [target_func]: 子线程执行中：{}".format(i))
        print("    [target_func]: 输入参数inp无任何返回")

    zprint("\n")
    zprint("case1： 超时时间为8秒，子线程运行耗时3秒， 预计三秒后子线程结束、主线程不再被block")
    t1 = TimeoutProcess(target=target_func, args=(30, 3), time_limit=8)
    result = t1.start()
    zprint("参数结果是 {}".format(result))
    zprint("\n")
    zprint("case1： 超时时间为8秒，子线程运行耗时3秒， 预计三秒后子线程结束、主线程不再被block, 无任何返回")
    t1 = TimeoutProcess(target=taget_no_return, args=(30, 3), time_limit=8)
    result = t1.start()
    zprint("参数结果是 {}".format(result))
    zprint("\n")
    zprint("case2： 超时时间为5秒，子线程运行耗时8秒， 预计五秒后主线程不再block，子线程被强制结束")
    t2 = TimeoutProcess(target=target_func, args=(30, 8), time_limit=5)
    res2 = t2.start()
    zprint("参数结果是 {}".format(res2))


if __name__ == '__main__':
    ExqUtils.parse_argv(['/Users/zac/server/mange_services_separate.py', '1', '2', '3', '4', '--sum', '3', '-delete', '3'])

    test_timeout_process()
    assert False
    test_timeout()
    assert False
    # 验证 timeit
    test_time_it()
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
