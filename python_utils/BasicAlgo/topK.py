##################################################
# topK问题
# 1. 直接排序取第k个，比如快排直接就是O(nlogn)的复杂度
# 2. O(n),利用快排的partition思想
##################################################


# O(n),利用快排的partition思想,在各个part中迭代查找
def find_topK(data_inp,k):
    b, data = data_inp[0], data_inp[1:]
    left, right = [],[]
    for i in range(len(data)):
        # 这里不能写<=b，如果出现重复的b，
        if data[i] < b:
            left.append(data[i])
        else:
            right.append(data[i])
    if len(left) == k-1:
        return left+[b]
    elif len(left) < k-1:
        return [b]+right
    todo


# 堆的思路，其实就是维护了一个额外的「存储对象」，每次保存k个元素
# 先取原数组的前k个，然后对这个「存储对象」排序（堆做下沉/上浮）
# 然后遍历原数组的k+1:-1，每次都把新元素插入并重新排序这个「存储对象」（即更新堆），截取其[:-2]的元素（保持长度为k）
# 假设用数组替代堆，用sorted替代下沉/上浮


nums_s=[0]*11
for i in range(0,len(nums_s),2):
    print(i)
for idx,i in enumerate(nums_s):
    print(idx,i)
    if idx == len(nums_s)-1:
        print(idx,i,"lasst")
    else:
        if i != nums_s[idx+1]:
            print(idx,nums_s[idx+1],i,"not e")
        else:
            pass
                