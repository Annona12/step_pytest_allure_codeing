# -*-encoding:utf-8-*-
from multiprocessing import Process, Manager
from time import sleep


def thread_a_main(sync_data_pool):  # A 进程主函数，存入100+的数
    for ix in range(100, 105):
        sleep(1)
        sync_data_pool.append(ix)


def thread_b_main(sync_data_pool):  # B 进程主函数，存入300+的数
    for ix in range(300, 309):
        sleep(0.6)
        sync_data_pool.append(ix)


def _test_case_000():  # 测试用例
    manager = Manager()  # multiprocessing 中的 Manager 是一个工厂方法，直接获取一个 SyncManager 的实例
    sync_data_pool = manager.list()  # 利用 SyncManager 的实例来创建同步数据池
    Process(target=thread_a_main, args=(
        sync_data_pool, )).start()  # 创建并启动 A 进程
    Process(target=thread_b_main, args=(
        sync_data_pool, )).start()  # 创建并启动 B 进程
    for ix in range(6):  # C 进程（主进程）中实时的去查看数据池中的数据
        sleep(1)
        print(sync_data_pool)


if '__main__' == __name__:  # 将测试用例单独列出
    _test_case_000()
