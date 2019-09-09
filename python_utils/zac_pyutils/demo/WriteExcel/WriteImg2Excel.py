# author: zac
# create-time: 2019-09-06 16:42
# usage: - 
import xlsxwriter as xw
import os
from io import BytesIO
from PIL import Image
import datetime


def get_image_as_bytes(img):
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes


########################
# 从文件中获取各种配置
########################
with open("./config.txt", "r") as fr:
    content = [i.strip().split("=") for i in fr.readlines() if not i.startswith("#")]
    content = {i[0]: "=".join(i[1:]) for i in content}

# fp = "/Users/zac/Downloads/tiles_demo.xlsx"
book_fp = "./demo.xlsx"
logo_left = Image.open("./logo_left.png")
logo_right = Image.open("./logo_right.png")
pic_dir = content['picsDir']
pic_type = ['.png', '.jpg', '.jpeg']
pic_fp_list = [os.path.join(pic_dir, i) for i in os.listdir(pic_dir) if os.path.splitext(i)[-1] in pic_type]

wb = xw.Workbook(book_fp)
ws1 = wb.add_worksheet("abc")
cell_w, cell_h = ws1.default_col_pixels, ws1.default_row_pixels
print(cell_w, cell_h)
logo_left = logo_left.resize((int(cell_w*(0.6+0.6)), int(cell_h*(0.5+2+0.5))))
logo_right = logo_right.resize((int(cell_w*(0.8+2+0.8)), int(cell_h*(0.5+2+0.5))))
#########
# 各种属性
#########
bold = wb.add_format({'bold': True})
title_format = wb.add_format({
    'bold': True,
    'font_name':'Calibri',
    'font_size': 18,
    'border': 6,
    'align': 'center',  # 水平居中
    'valign': 'vcenter',  # 垂直居中
    'fg_color': '#D7E4BC',  # 颜色填充
    'top': 2,
    'bottom': 2,
    'left': 2,
    'right': 2,

})
desc_format = wb.add_format({
    'bold': True,  # 加粗字体
    'font_name':'Calibri',
    'font_size': 12,
    'text_wrap': True,  # 默认就是True？
    'align': 'left',  # 水平居中
    'valign': 'vcenter',  # 垂直居中
    'fg_color': '#A9A9A9',  # 颜色填充
    'top': 2,  # 上边框宽度
    'bottom': 2,  # 下
    'left': 2,  # 左
    'right': 2,  # 右
})
generic_format = wb.add_format({
    'bold': True,  # 加粗字体
    'font_name':'Calibri',
    'font_size': 12,
    'text_wrap': True,  # 默认就是True？
    'align': 'left',
    'valign': 'vcenter',  # 垂直居中
    'top': 2,  # 上边框宽度
    'bottom': 2,  # 下
    'left': 2,  # 左
    'right': 2,  # 右
})
picName_format = wb.add_format({
    'bold': True,  # 加粗字体
    'font_name':'Calibri',
    'font_size': 16,
    'text_wrap': True,  # 默认就是True？
    'align': 'center',
    'valign': 'vcenter',  # 垂直居中
})

top_border_format = wb.add_format({
    'top': 2,  # 左
})
bottom_border_format = wb.add_format({
    'bottom': 2,  # 左
})
left_border_format = wb.add_format({
    'left': 2,  # 左
})
right_border_format = wb.add_format({
    'right': 2,  # 左
})
anchor_right_top_format = wb.add_format({"right":2,"top":2})
anchor_left_top_format = wb.add_format({"left":2,"top":2})
anchor_right_bottom_format = wb.add_format({"right":2,"bottom":2})
anchor_left_bottom_format = wb.add_format({"left":2,"bottom":2})
############
# 插入logo
############
print(logo_left.size, logo_right.size)
ws1.insert_image("A1", "left", options={'image_data': get_image_as_bytes(logo_left), 'x_offset' : int(cell_w*0.4), 'y_offset': int(cell_h*0.5)})
ws1.insert_image("O1", "right", options={'image_data': get_image_as_bytes(logo_right), 'x_offset': int(cell_w*0.2), 'y_offset': int(cell_h*0.5)})
for i in [0, 1, 14, 15, 16, 17]:
    ws1.write(0, i, "", top_border_format)
for i in range(0, 3 + 1):
    ws1.write(i, 0, "", left_border_format)
for i in range(0, 3 + 1):
    ws1.write(i, 17, "", right_border_format)
# 连接处要改一下
ws1.write(0, 17, "", anchor_right_top_format)  # 右上角
ws1.write(0, 0, "", anchor_left_top_format)  # 左上角
############
# 插入标题等
############
title = content['title']
description = content['description']
item = content['item']
engineer = content['engineer']

ws1.merge_range('C1:N4', title.strip(), title_format)
ws1.merge_range("A5:R9", description.strip(), desc_format)
ws1.merge_range("A10:I11", item.strip(), generic_format)
ws1.merge_range("J10:M11", engineer.strip(), generic_format)
tomorrow = datetime.date.today()+datetime.timedelta(days=1)
tomorrow = tomorrow if tomorrow.weekday() != 6 else tomorrow+datetime.timedelta(days=1)
date="Date: {}".format(tomorrow.strftime("%d/%m/%Y"))
ws1.merge_range("N10:R11", date.strip(), generic_format)


################
# 插入图片
################
cnt = 0
for fp in pic_fp_list:
    f_name = os.path.splitext(os.path.basename(fp))[0]
    img = Image.open(fp)
    # 图片：宽7个cell，高 16 个cell
    img = img.resize((int(cell_w*7), int(cell_h*16)))
    # 图片的边距：距离左边1个cell，距离上面 0个cell
    img_row, img_col = 12+cnt//2*(16+2), 0+cnt%2*9
    print("cnt-{} 图片坐标:".format(cnt), (img_row, img_col))
    ws1.insert_image(row=img_row, col=img_col, filename=f_name,
                     options={'image_data': get_image_as_bytes(img), 'x_offset': int(cell_w * 1)})
    # 图片的名字填在这里：注意这里下标是以0开始的 12 是图片放置的坐标(这里是0开始的，如果excel里看是第13行)
    first_row, first_col = 12 + 16 + cnt // 2 * (16 + 2), 0 + cnt % 2 * 9
    last_row, last_col = first_row + 2 - 1, first_col + 9 - 1  # 右下角的坐标相比左上角，高2宽9，为了得到坐标要减去1
    print("cnt-{} 文字坐标:".format(cnt), (first_row, first_col), (last_row, last_col))
    ws1.merge_range(first_row, first_col, last_row, last_col, data=f_name.strip(), cell_format=picName_format)
    cnt += 1
################
# 构造加厚的边框
################
# 竖着左边
for i in range(11,75+1):
    ws1.write(i,0,"",left_border_format)
# 竖着右边
for i in range(11,75+1):
    ws1.write(i,17,"",right_border_format)
# 横着下边
for i in range(0,17+1):
    ws1.write(75,i,"",bottom_border_format)
# 连接处要改一下
ws1.write(75,17,"",anchor_right_bottom_format) #右下角
ws1.write(75,0,"",anchor_left_bottom_format) #左下角

wb.close()
