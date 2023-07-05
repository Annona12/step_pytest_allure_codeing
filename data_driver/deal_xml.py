# 开发者：Annona
# 开发时间：2023/6/2 13:14
import random
import time
import xml.etree.ElementTree as ET

"""
该函数用来统一处理我们需要修改xml参数的方法
"""


def set_xml(xml_path, element_dic):
    """
    :param xml_path:该参数表示xml报文文件的地址
    :param element_dic:该参数表示需要修改的参数的字典
    :return:
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for element in element_dic:
        for i in root.iter(element):
            i.text = element_dic[element]
    tree.write('data/temp.xml',encoding='utf-8',xml_declaration=True)
def set_xml_string(xml_path):
    """
    :param xml_path:该参数表示xmlb报文文件的地址
    :return:返回读取的xml文件字符串
    """
    params_string = ''
    file = open(file=xml_path, mode='r', encoding='utf-8')
    element_list = file.readlines()
    for element in element_list:
        params_string += element
    return params_string
