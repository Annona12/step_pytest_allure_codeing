# 开发者：Annona
# 开发时间：2023/6/5 15:04
import xml.etree.ElementTree as ET

# 通过从文件中读取来导入此数据
tree = ET.parse('../data/DS_1101_SHG_Fix_XSCJ.xml')
root = tree.getroot()
for i in root.findall('header'):
    # print(i.text)
    root.remove(i)
tree.write('../data/DS_1101_SHG_Fix_XSCJ.xml')
# for i in root.findall('header'):
#     print(i.find('msgType').text,i.get('属性名字'))
# for i in root:
#     print(i.tag, i.attrib, i.text)
#     for j in i:
#         print(j.tag, j.attrib, j.text)
#         for k in j:
#             print(k.tag, k.attrib, k.text)
#             for q in k:
#                 print(q.tag, q.attrib, q.text)

# 直接从字符串中解析
# root = ET.fromstring()
#
#
# def __indent(elem, level=0):
#     i = "\n" + level * "\t"
#     if len(elem):
#         if not elem.text or not elem.text.strip():
#             elem.text = i + "\t"
#         if not elem.tail or not elem.tail.strip():
#             elem.tail = i
#         for elem in elem:
#             __indent(elem, level + 1)
#         if not elem.tail or not elem.tail.strip():
#             elem.tail = i
#     else:
#         if level and (not elem.tail or not elem.tail.strip()):
#             elem.tail = i
#
#
# root = ET.Element('root')
# tree = ET.ElementTree(root)
# name = Element("name")
# name.text = 'Annona'
# age = Element('age')
# age.text = '12'
#
# root.append(name)
# root.append(age)
# __indent(root)
# tree.write('test.xml', encoding='utf-8', xml_declaration=True)
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

# 读取xml文档
tree = ET.parse('../data/DS_1101_SHG_Fix_XSCJ.xml')
# 获取根节点
root = tree.getroot()

i = root.findall('header')
j = root.iter('orderType')
for k in j:
    print(k.text,k.tag,k.attrib)
print(root[0][1])
# print(list(root))
# print(root.tag)
# print(i)
# print(j)

