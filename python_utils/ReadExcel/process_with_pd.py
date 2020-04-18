import pandas as pd
import numpy as np

fp="/Users/zac/Downloads/潘书尚-毕业论文数据-2020315.xlsx" 
df_excel=pd.read_excel(fp,sheet_name="毕业论文-产业数据（剔除规划缺失的地级市）")
df_raw=df_excel.query("城市 == 城市")# 过滤掉城市这列为NaN的（NaN不等于任何，即它也不等于自己）
df_raw=df_raw.query("文件名称 != '缺失'")# 过滤掉城市这列为NaN的（NaN不等于任何，即它也不等于自己）
all_industry=["新一代信息技术产业","高端装备制造产业","新材料产业","生物产业","新能源汽车产业","新能源产业","节能环保产业"]
df=df_raw[["城市","分类"]+all_industry]
 

# 展示所有存在缺失值的
# nan_idx=[idx for idx,row in df.iterrows() if np.any(pd.isna(row).values)]
# df.loc[nan_idx]

df = df.fillna(0.0)
all_city_indust=[]
for row_idx, row in df.iterrows():
    values=row[all_industry].values if row['分类'] == "十二五" else [0]*len(all_industry)
    city_indust=[item_idx for item_idx,item in enumerate(values) if item>0]
    all_city_indust.append((row['城市'],city_indust))

res_series=[]
for row in all_city_indust:
    row_city,row_indust=row
    intersect_indust={}
    for col in all_city_indust:
        col_city,col_indust=col
        intersect_indust.update({col_city:len(set(row_indust).intersection(col_indust))})
    res_series.append(pd.Series(name=row_city,data=intersect_indust))

resDF=pd.DataFrame(res_series)
resDF.to_excel("abx.xlsx")


########################################
# 矩阵做比值
# 同构性的度量: 
# 该城与其他城市同构产业的 sum/avg/median
########################################
fp="/Users/zac/Downloads/潘书尚-毕业论文数据-2020315.xlsx" 
df_excel=pd.read_excel(fp,sheet_name="毕业论文-相邻矩阵（十三五）")
all_cities=list(df_excel['城市'])
res=[]
for idx,row in df_excel.iterrows():
    res.extend([(row['城市'],city,row[city]) for city in all_cities[idx:]])
df_res=pd.DataFrame(res,columns=["city1","city2","isomo"])
df_res.to_excel("abc.xlsx")

fp="/Users/zac/Downloads/潘书尚-回归数据.xlsx"
fp="/Users/zac/Downloads/潘书尚-回归数据-final.xlsx"
df_excel=pd.read_excel(fp,sheet_name="2011变量")
# fields=["rgdp","pop","财政支出","人口密度","专利数","企业所得税","外商投资额","规模以上工业总产值","预算内财政收入","第三产业占比"]
fields=["rgdp","pop","财政支出","人口密度","专利数","企业所得税","外商直接投资额","财政收入","规模以上工业总产值","第三产业占比"]
arr=np.array(df_excel[['c']+fields])
res=[]
for i in range(arr.shape[0]):
    city_i,values_i=arr[i][0],arr[i][1:]
    for j in range(i,arr.shape[0]):
        city_j,values_j=arr[j][0],arr[j][1:]
        res_dict=dict(zip(fields,
                          [p[0]/p[1] if p[1]!=0 else None for p in zip(values_i,values_j)]))
        res_dict.update({"city1":city_i,"city2":city_j})
        res.append(res_dict)
resDF=pd.DataFrame(res)
resDF=resDF[['city1','city2']+fields]
resDF.count()
fileds_with_NA=["规模以上工业总产值","外商直接投资额"]
for field in fileds_with_NA:
    resDF[field]=resDF[field].fillna(resDF[field].max())
resDF.count()
resDF.to_excel("indep_2011.xlsx")



fp = "/Users/zac/Downloads/50连线城市.xlsx"
df1=pd.read_excel(fp,sheet_name="所属省份")
df2=pd.read_excel(fp,sheet_name="所有地级市平均距离")
all_province = df1['prov']
res=[]
for k,g in df1.groupby("prov"):
    # print("at province: ",k)
    dist_list=[]
    for c1 in g['c']:
        for c2 in g['c']:
            dist=df2.query(f"(city1=='{c1}' and city2=='{c2}') or (city1=='{c2}' and city2=='{c1}')")['dist_km'].iloc[0]
            # print(c1,c2,dist)
            dist_list.append(dist)
    dist_avg = sum(dist_list)/len(dist_list)
    res.append((k,dist_avg))

print("省内城市距离均值:")
print("\n".join([k+", "+str(round(v,1)) for k,v in res]))
print("各省的「省内•城市距离均值」的均值:")
am = [v for k,v in res if v != 0]
print(sum(am)/len(am))

