# 对排序后的数组建立huffman树
# 排好序意味着可以把新计算的父节点做「二分插入」

class Node():
    def __init__(self,v,l=None,r=None):
        self.l=l
        self.r=r
        self.v=v

def binary_insert_node(arr,node,start=None,end=None):
    if start is None:
        start=0
    if end is None:
        end=len(arr) -1 
    mid = (start+end)//2
    if arr[mid].v == node.v:
        return arr[start:mid+1] + [node] + arr[mid+1:end+1]
    elif arr[mid].v < node.v:
        if arr[end].v < node.v:
            return arr[start:end+1] + [node]
        return arr[start:mid+1] + binary_insert_node(arr,node,start=mid+1,end=end)
    elif node.v < arr[mid].v:
        if node.v < arr[start].v:
            return [node] + arr[start:end+1]
        return binary_insert_node(arr,node,start=start,end=mid-1) + arr[mid:end+1]
    else:
        assert False

items=[1,2,3,4,5,6,7,8,9]
# items=[1,2,3,4]
nodes=[Node(v=i) for i in items]
print(f"nodes value: {[i.v for i in nodes]}")
print("循环取前两个最小的建树，并将父节点放回原数组（二分插入）")
while len(nodes)>1:
    print(f"  len(nodes): {len(nodes)}")
    l,r = nodes.pop(0),nodes.pop(0)
    p=Node(v=l.v+r.v,l=l,r=r)
    if len(nodes) == 0:
        print(f"    nodes value after pop2: []")
        break
    print(f"    nodes value after pop2: {[i.v for i in nodes]}")
    nodes=binary_insert_node(nodes,p)
    print(f"    nodes value after insert: {[i.v for i in nodes]}")

print("根节点: ",p,p.v)
def print_node(nodes):
    print(f"{[i.v if i is not None else None for i in nodes]}")
to_print=[p]
while len(to_print)>0:
    print_node(to_print)
    tmp = []
    for i in to_print:
        if i is not None:
            tmp.extend([i.l,i.r])
    to_print=tmp


        

