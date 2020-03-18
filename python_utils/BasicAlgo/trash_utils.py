def quick_sort(data_inp):
    # 错误点有二
    # 1. 取了第一个锚定点b之后，data要更新为剩余的数据不然会出现b自己和自己比
    # 2. 终止递归的条件是 <=1 因为最后b就和一个数比，要么是left里的要么是right里的，left/right必然有一个是空的
    b, data = data_inp[0],data_inp[1:]
    left,right=[],[]
    for i in range(len(data)):
        if data[i]==b:
            # to fix
            left.append(data[i])
        elif data[i] < b:
            left.append(data[i])
        elif data[i] > b:
            right.append(data[i])
        else:
            assert False,"unexcepted assert"
    left = left if len(left) <= 1 else quick_sort(left)
    right = right if len(right) <= 1 else quick_sort(right)
    return left+[b]+right

def test_quick_sort(data=None):
    if data is None:
        data=[8,4,3,2,9,1,12,14]
    print(">>> [test-case] 测试快速排序")
    print("原数组如下:")
    print("length:",len(data), "data:", data)
    print("排序后的数组如下:")
    print(quick_sort(data))


def random_choice(data_inp,k):
    data = data_inp.copy()
    import random
    lth=len(data)
    res=[]
    try:
        # 思路主要是
        # 每次随机一个 0~len(data) 的整数作为索引，取一个元素到res数组
        # 每取一个数后数组会更新为剩余值（扣掉被取走元素的idx）
        # 循环到res数组长度等于目标k
        for i in range(lth):
            target_idx=random.randint(0,lth-1-i)
            res.append(data[target_idx])
            if target_idx == 0:
                data = data[1:]
            elif target_idx == lth-1-i:
                data = data[:target_idx]
            else:
                data = data[:target_idx]+data[target_idx+1:]
            if len(res) >= k:
                break
    except Exception as e:
        print(e)
        print(f"i: {i}, target_idx: {target_idx}")
    return res

def test_random_choice(data=None):
    if data is None:
        data = [2,3,4,5,6,7,8,9]
    print(">>> [test-case] 测试从数组中随机选择整个数组长度的元素（数组随机重排）")
    print("原数组如下:")
    print("length:",len(data), "data:", data)
    m=[random_choice(data,len(data)) for i in range(1000)]
    print(set([len(m) for i in m]))
    print("随机抽三个random_choice的结果如下:")
    _ = [print(i) for i in random_choice(m,3)]


def heap_sort(data_inp):
    def heapify(arr,n,i):
        pass
    pass

if __name__ == "__main__":
    test_random_choice()

    test_quick_sort()










