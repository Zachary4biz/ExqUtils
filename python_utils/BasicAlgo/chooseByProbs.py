import random
x=[1,2,3,4,5]
probs=[0.1,0.2,0.1,0.2,0.4]

# 把概率理解为长度为0.1 0.2的线段，合到一起长度为1
# 第一个元素的概率0.1 => 随机数落在(0, 0.1]之间（区间长度为0.1）
# 第二个元素的概率0.2 => 随机数落在(0.1,0.3]之间（区间长度为0.2）
# 第三个元素的概率0.1 => 随机数落在(0.3,0.4]之间（区间长度为0.1）
# 以此类推
def prepare(probs_inp):
    return [sum(probs_inp[:idx+1]) for idx in range(len(probs_inp))]

# 二分查找判断随机数在哪个区间
def search(probs_inp,t,start=None,end=None):
    start = 0 if start is None else start
    end = len(probs_inp)-1 if end is None else end
    mid = (start+end)//2
    if mid == start:
        # 这个边界条件是说，当start end是连续的时候，如(3,4)、(0,1)这种时候说明区间已经锁定了直接返回end就是目标索引
        return end
    if probs_inp[mid-1] < t and t <= probs_inp[mid]:
        return mid
    elif probs_inp[mid] <= t:
        return search(probs_inp,t,start=mid,end=end)
    elif probs_inp[mid] > t:
        return search(probs_inp,t,start=start,end=mid)

def sample(x,probs_inp):
    probs=prepare(probs_inp)
    t = random.randint(0,10)/10.0
    idx = search(probs,t)
    return idx,x[idx]

print(sample(x,probs))
