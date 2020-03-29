arr = [3,3,4,6,7,5,5,7]
def forward(arr,n,i=None):
    if i is None:
        i=0
    if i>=n:
        return
    l = 2*i+1
    r = 2*i+2
    print(i,arr[i])
    forward(arr,n,i=l)
    forward(arr,n,i=r)
print("前序遍历",arr)
forward(arr,len(arr))

def mid(arr,n,i=None):
    if i is None:
        i=0
    if i>=n:
        return
    l = 2*i+1
    r = 2*i+2
    mid(arr,n,i=l)
    print(i,arr[i])
    mid(arr,n,i=r)
print("中序遍历",arr)
mid(arr,len(arr))


def back(arr,n,i=None):
    if i is None:
        i=0
    if i>=n:
        return
    l = 2*i+1
    r = 2*i+2
    back(arr,n,i=l)
    back(arr,n,i=r)
    print(i,arr[i])
print("后序遍历",arr)
back(arr,len(arr))


def pre_stack(arr,n,i=None):
    if i is None:
        i=0
    stack = [i]
    while len(stack)>0:
        node = stack.pop()
        print(node,arr[node])
        l = 2*node+1
        r = 2*node+2
        if r < n:
            stack.append(r)
        if l < n:
            stack.append(l)
print("前序遍历 | 非递归")
pre_stack(arr,len(arr))

def back_stack(arr,n,i=None):
    if i is None:
        i=len(arr)-1 
    stack = [i]
    while len(stack)<n:
        node = stack[-1]
        l = 2*node+1
        r = 2*node+2
        if r < n:
            stack.append(r)
        if l < n:
            stack.append(l)
    while len(stack)>0:
        node = stack.pop()
        print(node,arr[node])
print("后序遍历 | 非递归")
back_stack(arr,len(arr))


