# 开发者：Annona
# 开发时间：2023/12/28 10:54
import datetime
import os

from constant.constant import QDBJ_URL, MY_LOGGER

# 全局变量作为缓存
cache = {}


def read_shg_fix_file(file_url, file_name='ZQ_QDBJ'):
    """
    读取并解析上交所确定报价等文件
    :param file_url: 确定报价的文件的地址（即报盘下载文件的地址）
    :param file_name: 需要解析的文件名，默认需要解析的文件为ZQ_QDBJ
    :return:
    """
    # 定义全局的缓存数据
    global cache
    file_date = datetime.datetime.now().strftime('%Y%m%d')
    full_file_name = file_name + file_date + '.txt'
    file_path = os.path.join(file_url, full_file_name)
    try:
        with open(file_path, 'r') as file:
            file_list = file.readlines()
            list_length = len(file_list)
            hq_list = []
            hq_dict = {}
            hq_dict['time'] = file_list[0]
            hq_list.append(hq_dict)
            # for i in range(1, list_length):
            #     item = file_list[i].replace(' ', '').split('|')
            #     for i in range(len(item)):
            #         if i == 0:
            #             hq_dict['证券代码'] = item[i]
            #         elif i == 1:
            #             hq_dict['证券简称'] = item[i]
            #         elif i == 2:
            #             hq_dict['买入订单编号'] = item[i]
            #         elif i == 3:
            #             hq_dict['买入报价时间'] = item[i]
            #         elif i == 4:
            #             hq_dict['买入报价方'] = item[i]
            #         elif i == 5:
            #             hq_dict['买入价（净价）'] = item[i]
            #         elif i == 6:
            #             hq_dict['买入数量（手）'] = item[i]
            #         elif i == 7:
            #             hq_dict['买入全价'] = item[i]
            #         elif i == 8:
            #             hq_dict['买入到期收益率'] = item[i]
            #         elif i == 9:
            #             hq_dict['卖出订单编号'] = item[i]
            #         elif i == 10:
            #             hq_dict['卖出报价时间'] = item[i]
            #         elif i == 11:
            #             hq_dict['卖出报价方'] = item[i]
            #         elif i == 12:
            #             hq_dict['卖出价（净价）'] = item[i]
            #         elif i == 13:
            #             hq_dict['卖出数量（手）'] = item[i]
            #         elif i == 14:
            #             hq_dict['卖出全价'] = item[i]
            #         elif i == 15:
            #             hq_dict['卖出到期收益率'] = item[i]
            #         elif i == 16:
            #             hq_dict['应计利息'] = item[i]
            #     hq_list.append(hq_dict)
    except Exception as e:
        MY_LOGGER.error(e)
    cache['data'] = hq_list
    MY_LOGGER.info(cache['data'])
    return hq_list


# 从缓存中获取数据
def get_date_from_cache():
    global cache
    # 从缓存中获取数据
    data = cache.get('data')
    return data


read_shg_fix_file(QDBJ_URL)
