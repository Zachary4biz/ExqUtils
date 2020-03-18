
def findRepeatNumber(nums):
    tmp={}
    for i in nums:
        if i in tmp:
            return i
        else:
            tmp[i]=0
    return None

# 所谓O(1)的空间复杂度，原地排序+二分查找
def findRepeatNumberV2(nums):
    pass


data = [1,0,2,4,5,3,2,19,344,532]
print(findRepeatNumber(data))