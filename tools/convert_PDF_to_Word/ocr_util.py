# -*- encoding: utf-8 -*-
"""
@author: Aramil
@date: 2023/5/10 14:57
@brief: ocr工具
"""


def xy_info(results):
    data_list = []
    for result in results:
        print("result:", result)
        for res in result:
            info = res[1][0]
            boxx, boxy = res[0][0]
            data_list.append([info, int(boxx), int(boxy)])

    return data_list
