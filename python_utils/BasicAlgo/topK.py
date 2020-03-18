##################################################
# topK问题
# 1. 直接排序取第k个，比如快排直接就是O(nlogn)的复杂度
# 2. O(n),利用快排的partition思想
##################################################


# O(n),利用快排的partition思想,在各个part中迭代查找
def find_topK(data_inp,k):
    data = data_inp.copy()
    b = data.pop()
    left, right = [],[]
    for i in data:
        if i < b:
            left.append(i)
        else:
            right.append(i)
    if len(right) == k:
        return right
    elif len(right) == k-1:
        return [b]+right
    elif len(right) < k-1:
        return find_topK(left,k-1-len(right))+[b]+right
    elif len(right) > k:
        return find_topK(right,k)
    else:
        assert False, "unexcepted err"

# 堆的思路，其实就是维护了一个额外的「存储对象」，每次保存k个元素
# 先取原数组的前k个，然后对这个「存储对象」排序（堆做下沉/上浮）
# 然后遍历原数组的k+1:-1，每次都把新元素插入并重新排序这个「存储对象」（即更新堆），截取其[:-2]的元素（保持长度为k）
# 假设用数组替代堆，用sorted替代下沉/上浮



data = [1,95,274,4,23,19,33,22,44]
print(">>> ori data:")
print(data)
print(sorted(data))
print(">>> topK")
print(find_topK(data,4))
