from threading import Thread
import time
import random
from queue import Queue
from collections import deque

# 创建队列，设置队列最大数限制为3个
queue = Queue(3)


# 生产者线程
class Pro_Thread(Thread):
    def run(self):
        # 原材料准备，等待被生产
        tasks = deque([1, 2, 3, 4, 5, 6, 7, 8])
        global queue
        while True:
            try:
                # 从原材料左边开始生产，如果tasks中没有元素，调用popleft()则会抛出错误
                task = tasks.popleft()
                queue.put(task)
                print("生产", task, "现在队列数:", queue.qsize())

                # 休眠随机时间
                time.sleep(random.random())
            # 如果原材料被生产完，生产线程跳出循环
            except IndexError:
                print("原材料已被生产完毕")
                break
        print("生产完毕")


# 消费者线程
class Con_Thread(Thread):
    def run(self):
        global queue
        while True:
            if not queue.empty():
                # 通过get(),这里已经将队列减去了1
                task = queue.get()
                time.sleep(2)
                # 发出完成的信号，不发的话，join会永远阻塞，程序不会停止
                queue.task_done()
                print("消费", task)
            else:
                break
        print("消费完毕")


# r入口方法，主线程
def main():
    Pro_1 = Pro_Thread()
    # 启动线程
    Pro_1.start()
    # 这里休眠一秒钟，等到队列有值，否则队列创建时是空的，主线程直接就结束了，实验失败，造成误导
    time.sleep(1)
    for i in range(2):
        Con_i = Con_Thread()
        # 启动线程
        Con_i.start()
    global queue
    # 接收信号，主线程在这里等待队列被处理完毕后再做下一步
    queue.join()
    # 给个标示，表示主线程已经结束
    print("主线程结束")


if __name__ == '__main__':
    main()