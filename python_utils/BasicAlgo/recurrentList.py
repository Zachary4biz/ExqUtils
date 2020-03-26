########################################
# 循环数组查询问题
# 循环有序数组：
# 指的是，将一个有序数组循环左/右移动若干距离之后变成的数组。
# 如，[1,2,3,4,5]循环右移3位，就成为[4,5,1,2,3]。
# 该数组的特点是，其中包含着一个转折点。转折点左右两侧的子数组都是有序的，并且左侧的子数组整体都比右侧的子数组大。
########################################
def binary_search(arr,target,start=None,end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(arr) - 1
    mid = (start+end)//2
    if arr[mid] == target:
        return mid
    if start >= end:
        print(start,end,"not found")
        return None
    if arr[mid] < target:
        return binary_search(arr,target,start=mid+1,end=end)
    elif target < arr[mid]:
        return binary_search(arr,target,start=start,end=mid-1)
    else:
        assert False

def search(arr,target,start=None,end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(arr) - 1
    mid = (start+end)//2
    if arr[mid] == target:
        return mid
    if start >= end:
        print(start,end,"not found")
        return None
    # start mid end 是升序，普通二分就行
    if arr[start] < arr[mid] and arr[mid] < arr[end]:
        if target < arr[mid]:
            return binary_search(arr,target,start=start,end=mid-1)
        else:
            return binary_search(arr,target,start=mid+1,end=end)
    # start mid end 先升再降，说明转折点在mid右边，mid的左边是升序
    elif arr[start] < arr[mid] and arr[mid] > arr[end]:
        if arr[start] < target and target < arr[mid]:
            return binary_search(arr,target,start=start,end=mid-1)
        else:
            return search(arr,target,start=mid+1,end=end)
    # start mid end 先降再升, 转折点在mid左边，mid的右边是升序
    elif arr[start] > arr[mid] and arr[mid] < arr[end]:
        if arr[mid] < target and target < arr[end]:
            return binary_search(arr,target,start=mid+1,end=end)
        else:
            return search(arr,target,start=start,end=mid-1)
    else:
        print(start,mid,end)
        print(arr[start],arr[mid],arr[end])
        assert False

reArr=[19,20,21,22,23,24,1,2,3,4,5]
target = 21
print("binary_search_res: [idx]:",binary_search([1,2,3,4,5],5))
print("search_res: [idx]:",search(reArr,5))
