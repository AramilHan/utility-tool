# -*- encoding: utf-8 -*-
"""
@author: Aramil
@date: 2023/5/10 14:14
@brief: 将PDF转换为Word
"""
import datetime
import os
import fitz
from paddleocr import PaddleOCR
import ocr_util
import re


# 将PDF转换为图片
def pyMuPDF_fitz(pdf_path, image_path):
    """
    :param pdf_path: pdf 地址
    :param image_path: 图片地址
    """
    print("="*5, "\tStart converting PDF to img.\t", "="*5)
    # 开始时间
    start_time_pdf2img = datetime.datetime.now()
    print("="*5, start_time_pdf2img, "="*5)
    print("image_path=" + image_path)
    pdf_doc = fitz.open(pdf_path)
    print("page_count=" + str(pdf_doc.pageCount))
    # 使用其中一页做测试
    for pg in range(13, 14):
        page = pdf_doc[pg]
        rotate = 0
        zoom_x = 20
        zoom_y = 20
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(image_path):
            os.makedirs(image_path)

        pix.writePNG(image_path + '/' + 'images_{}.png'.format(pg))

    # 结束时间
    end_time_pdf2img = datetime.datetime.now()
    print("="*5, end_time_pdf2img, "="*5)
    print("pdf2img时间=", (end_time_pdf2img - start_time_pdf2img).seconds)


def traversal_file(image_path, out_path):
    dir_list = os.listdir(image_path)
    for i in range(0, len(dir_list)):
        path = os.path.join(image_path, dir_list[i])
        file_name = dir_list[i][:-4]
        print(file_name)
        ocr_img(path, file_name, out_path)


def ocr_img(path, name, out_path):
    print("="*5, "\tStart converting img to Word.\t", "="*5)
    # 开始时间
    start_time_img2word = datetime.datetime.now()
    print("="*5, start_time_img2word, "="*5)
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    result = ocr.ocr(path, cls=False)
    xy_info = ocr_util.xy_info(result)
    print(xy_info)
    # xy_info.sort(key=lambda x: -x[1])
    # print(xy_info)

    datas = []
    for xy in xy_info:
        datas.append(xy[0])
        # if (len(xy[0]) > 4) and re.match(r'[\u4e00-\u9fa5]+', xy[0], re.S):
        #     datas.append(xy[0])
        # else:
        #     print(xy[0])

    if datas:
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        file_path = os.path.join(out_path, name+'.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            for line in datas:
                f.write(line + '\n')

    # 结束时间
    end_time_img2word = datetime.datetime.now()
    print("=" * 5, end_time_img2word, "=" * 5)
    print(name, "时间消耗", (end_time_img2word - start_time_img2word).seconds, 'S')


if __name__ == '__main__':
    pdf_path = '../../data/files/test.pdf'
    image_path = '../../data/test/image'
    out_path = '../../data/test/words'
    # pyMuPDF_fitz(pdf_path, image_path)
    traversal_file(image_path, out_path)
