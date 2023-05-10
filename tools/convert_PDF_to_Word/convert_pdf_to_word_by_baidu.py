# -*- encoding: utf-8 -*-
"""
@author:
@date: 2023/5/10 17:18
@brief:
"""
import fitz
from aip import AipOcr
import time
import docx
from docx.oxml.ns import qn

APP_ID = "xxxxxx"
API_KEY = "xxxxxx"
SECRET_KEY = "xxxxxx"

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def pdf_image(pdfPath, imgPath, zoom_x=5, zoom_y=5, rotation_angle=0):
    # 获取pdf文件名称
    name = pdfPath.split("/")[-1].split('.pdf')[0]
    # 打开PDF文件
    pdf = fitz.open(pdfPath)
    # 获取pdf页数
    num = pdf.page_count
    print(num)
    # 逐页读取PDF
    for pg in range(13, 14):
        page = pdf[pg]
        # 设置缩放和旋转系数
        trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        # 开始写图像
        pm.save(imgPath + name + "_" + str(pg) + ".png")
    pdf.close()
    return name, num


'''
将图片读取为docx文件
imgPath 图像所在路径
生成的docx也保存在图像所在路径中
name为pdf名称（不含后缀）
num为pdf页数
name和num均可由上一个函数返回

'''


def ReadDetail_docx(imgPath, name, num):
    # 建立一个空doc文档
    doc = docx.Document()
    # 设置全局字体
    doc.styles["Normal"].font.name = u"宋体"
    doc.styles["Normal"]._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    # 读取图片
    for n in range(13, 14):
        i = open(imgPath + name + "_" + str(n) + ".png", 'rb')
        time.sleep(0.1)
        img = i.read()
        message = client.general(img)
        print(message)
        content = message.get('words_result')
        # 将内容写入doc文档
        for i in range(len(content)):
            print(content[i])
            doc.add_paragraph(content[i].get('words'))
    # 保存doc文档
    doc.save(imgPath + name + '.docx')


def pdf_to_docx(pdfPath, imgPath, zoom_x=5, zoom_y=5, rotation_angle=0):
    print("正在将pdf文件转换为图片...")
    # 调用函数一将pdf转换为图片，并获得文件名和页数
    name_, num_ = pdf_image(pdfPath, imgPath, zoom_x, zoom_y, rotation_angle)
    print("转换成功！")
    print("正在读取图片内容...")
    # 调用函数二逐页读取图片并逐行保存在docx文件中
    ReadDetail_docx(imgPath, name_, num_)
    print("名为 {}.pdf 的pdf文件共有{}页，已成功转换为docx文件！".format(name_, num_))


# pdf储存路径
pdf_path = "../../data/files/test.pdf"
# 图片和生成的docx文件的储存路径
img_path = "../../data/baidu/test/result"
# 调用函数
pdf_to_docx(pdf_path, img_path)
