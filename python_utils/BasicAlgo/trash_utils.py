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
    print("\n\n>>> [test-case] 测试快速排序")
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
    print("\n\n>>> [test-case] 测试从数组中随机选择整个数组长度的元素（数组随机重排）")
    print("原数组如下:")
    print("length:",len(data), "data:", data)
    m=[random_choice(data,len(data)) for i in range(1000)]
    print(set([len(m) for i in m]))
    print("随机抽三个random_choice的结果如下:")
    _ = [print(i) for i in random_choice(m,3)]


def heapify(arr, n, i):
    #i: 当前要检查的元素（看它和它的子孙节点是否组成了最大堆）
    #n: 最大索引（i元素所有子孙的索引最大不超过这个索引）
    largest = i  
    # 表示第i个元素的左右节点，比如0的左右节点是(1,2)，1的左右节点是(3,4)，2的左右节点是(5,6)
    l = 2 * i + 1     # left = 2*i + 1 
    r = 2 * i + 2     # right = 2*i + 2 
    # 如果当前元素arr[i]小于arr[l]就把largest的索引替换为l; l<n 保证索引不会溢出
    if l < n and arr[largest] < arr[l]: 
        largest = l 
    # 同理，如果此时的arr[largest]还小于arr[r]，更新largest索引为r
    if r < n and arr[largest] < arr[r]: 
        largest = r 
  
    if largest != i: 
        print(f"  [heapify]将交换 arr[{i}]={arr[i]} 和 arr[{largest}]={arr[largest]}")
        arr[i],arr[largest] = arr[largest],arr[i]  # 交换
        heapify(arr, n, largest) 
  
def heapSort(arr): 
    n = len(arr) 
  
    print("初始数组为: ", arr)
    # Build a maxheap. 
    for i in range(n, -1, -1): 
        # 从数组[n-1]开始，做这个倒着查的原因就类似于从二叉树的底部叶子节点开始查一样
        heapify(arr, n, i) 
    print("heapify结果: ", arr)


    # 一个个交换元素
    for i in range(n-1, 0, -1): 
        # 把根节点放到数组“最后” | 这个“最后”随i变化，从n-1减小到1
        # 相当于把最大的元素和最小或第二小的数交换了
        print("  [交换取最大]当前数组为: ",arr)
        arr[i], arr[0] = arr[0], arr[i]   # 交换
        print(f"  [交换取最大]根节点(arr[0])放到\"最后\"(arr[{i}]): ", arr)
        # 拿掉根节点后的剩余元素在进行heapify(所以要设定此时heapify只用前i个元素来做)
        heapify(arr, i, 0) 
  
def test_heapSort():
    print ("\n\n>>> [testcase] 堆排序") 
    arr = [ 9,8,7,19,2,1,30,12, 11, 13, 5, 6, 7] 
    # arr = [3,5,4]
    heapSort(arr)
    print(arr)


def binary_insert(arr,item,start=None,end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(arr)-1
    mid = (start+end)//2
    if item < arr[start]:
        return [item] + arr[start:end+1]
    elif item > arr[end]:
        return arr[start:end+1] + [item]
    if mid == start:
        # start=end-1时，二者连续，那item就插在中间就行
        return arr[start:start+1] + [item] + arr[end:end+1]
    if arr[mid] == item:
        return arr[start:mid] + [item] + arr[mid:end+1]
    elif arr[mid] < item:
        return arr[start:mid] + binary_insert(arr,item,start=mid,end=end)
    elif arr[mid] > item:
        return binary_insert(arr,item,start=start,end=mid) + arr[mid+1:end+1]
    else:
        assert False

def test_binary_insert():
    print(">>> [testcase] 二分插入")
    items=[1,2,3,4,5,6,7,8,9]
    insert_item=0.5
    print("原数组: ",items)
    print("插入元素: ",insert_item)
    print(binary_insert(items,insert_item))

if __name__ == "__main__":
    test_random_choice()

    test_quick_sort()

    test_heapSort()

    test_binary_insert()
    










