# 开发者：Annona
# 开发时间：2023/6/2 13:14
import logging
import xml.etree.ElementTree as ET

from constant.constant import *

"""
该函数用来统一处理我们需要修改xml参数的方法
"""


def set_xml(xml_path, element_dic):
    """
    :param xml_path:该参数表示xml报文文件的地址
    :param element_dic:该参数表示需要修改的参数的字典
    :return:
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        print(element_dic)
        for element, value in element_dic.items():
            for ele in root.iter(element):
                ele.text = value
        tree.write('data/temp.xml', encoding='utf-8', xml_declaration=True)
        MY_LOGGER.info('组装报文完成！')
    except Exception as e:
        print(e)
        MY_LOGGER.error('修改XML参数失败:')
        MY_LOGGER.error(str(e))


def set_xml_string(xml_path):
    """
    :param xml_path:该参数表示xmlb报文文件的地址
    :return:返回读取的xml文件字符串
    """
    try:
        with open(xml_path, mode='r', encoding='utf-8') as file:
            params_string = file.read()
        MY_LOGGER.info('读取XML完成！')
        return params_string
    except Exception as e:
        MY_LOGGER.error('读取XML文件失败: ')
        MY_LOGGER.error(str(e))
