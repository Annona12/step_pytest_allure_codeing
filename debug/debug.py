import threading
import time

# 自动化测试任务
def run_test_task():
    # 执行自动化测试任务的代码
    print("自动化测试任务开始")
    time.sleep(5)  # 模拟测试任务的执行时间
    print("自动化测试任务结束")

# 定时查询行情任务
def run_query_task():
    # 执行定时查询行情任务的代码
    print("定时查询行情任务开始")
    time.sleep(3)  # 模拟查询任务的执行时间
    print("定时查询行情任务结束")

# 创建线程
test_thread = threading.Thread(target=run_test_task)
query_thread = threading.Thread(target=run_query_task)

# 启动线程
test_thread.start()
query_thread.start()

# 等待线程结束
test_thread.join()
query_thread.join()

print("所有任务完成")