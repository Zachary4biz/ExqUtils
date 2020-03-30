def editDist(a,b):
    m,n=len(a)+1,len(b)+1
    mat = [[0 for _ in range(n)] for _ in range(m)]
    for j in range(n):
        mat[0][j] = j
    for i in range(m):
        mat[i][0] = i
    for i in range(m):
        for j in range(n):
            if i == 0:
                mat[i][j] = j
            elif j == 0:
                mat[i][j] = i
            else:
                if a[i-1] == b[j-1]:
                    mat[i][j] = mat[i-1][j-1]
                else:
                    mat[i][j] = min(mat[i-1][j-1]+2,mat[i-1][j]+1,mat[i][j-1]+1)
    return mat[-1][-1]

editDist("edit","edot")
