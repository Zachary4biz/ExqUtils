############
# 找公共子串
# 
############
import numpy as np

# 给dp的矩阵加上一行、一列，填充的是目标字符串，方便log查看日志
def add_to_log(matrix,a,b):
    matrix_to_log = np.array(matrix)
    matrix_to_log = np.hstack((np.array(list(b)).reshape(-1,1),matrix_to_log))
    matrix_to_log = np.vstack((np.array(list(" "+a)).reshape(1,-1),matrix_to_log))
    return matrix_to_log

def find(a,b):
    info=(0,0,0) # row,col,len
    matrix=[[0]*len(a) for _ in range(len(b))]
    print(">>> 先初始化全0矩阵，shape是 len(a)xlen(b)")
    print(add_to_log(matrix,a,b))
    for idx,i in enumerate(matrix[0][:]):
        matrix[0][idx]= 1 if a[idx] == b[0] else 0
    for idx,i in enumerate(matrix[:][0]):
        matrix[idx][0]= 1 if b[idx] == a[0] else 0
    print(">>> 为方便计算需要先初始化第一行和第一列")
    print(add_to_log(matrix,a,b))
    for idx_i,i in enumerate(a):
        if idx_i == 0 :
            continue
        for idx_j,j in enumerate(b):
            if idx_j == 0:
                continue
            if i==j:
                matrix[idx_j][idx_i] = matrix[idx_j-1][idx_i-1]+1
                if matrix[idx_j][idx_i] > info[-1]:
                    info = (idx_j,idx_i,matrix[idx_j][idx_i])
            else:
                matrix[idx_j][idx_i] = 0

    print(">>> 逐行逐列计算，当前b[j]==a[i]时矩阵的值为左上角值再加一")
    print(add_to_log(matrix,a,b))
    print(f">>> 最长公共子串 长度是 {info[2]}, 结尾字符在b[{info[0]}] a[{info[1]}]")
    print(f">>> 最长公共子串是: {a[info[1]-info[2]+1:info[1]+1]}")
    return (a[info[1]-info[2]+1:info[1]+1],info[-1])

# find("akicoks","kiovsicoaciis")



##########
# KMP
##########

s2="abcdefg"
m=len(s2)
next = [-1 for i in range(m)]
for i in range(1, m):
    k = next[i - 1]
    while k != -1 and s2[k] != s2[i - 1]:
        k = next[k]
    next[i] = k + 1


####################
# 回文问题
# 正反读都是一样的字符
# https://zhuanlan.zhihu.com/p/38251499
####################

# 找出最大的回文串
# 1. 可以看成是字符串反过来之后（取[::-1]）再和自己取最大公共子串
#    但是会存在一些特殊的情况下是错误的 比如 abacmkcaba
#    正向：abacmkcaba
#    取反：abackmcaba
#    交集：abac  这不是回文

inps="abagkildlikgaba"
palin=""
for i in range(1,len(inps)):
    palin_tmp=inps[i]
    for j in range(1,i+1):
        if i-j < 0 or i+j >= len(inps):
            break
        if inps[i-j] == inps[i+j]:
            palin_tmp=inps[i-j]+palin_tmp+inps[i+j]
        else:
            break
    if len(palin_tmp) > len(palin):
        palin = palin_tmp














