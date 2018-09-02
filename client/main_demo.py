import time
import threading
import runCamera
import generateQRCode
import piGPIO
import rGUI
import os

# 设置GPIO
triggerPin = 16  # 拍照触发按键
fanPin = 18  # 风扇输出
lightPin = 22  # 灯输出
piGPIO.pinSetup(triggerPin, fanPin, lightPin)

# 全局变量
triggerFlag = False
rGUI_visible = False
exitFlag = 0

# 线程_GUI
def run_rGUI():
    rGUI.run_Self()

# 默认线程class
class myThread(threading.Thread):
    def __init__(self, threadID, name, freq):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.freq = freq

    def run(self):
        print("开启线程： " + self.name)
        print_time(self.name, self.freq, 1)
        print("退出线程： " + self.name)

# 线程_检测按键
class thread_pinDetective(myThread):
    def run(self):
        while True:
            if piGPIO.readPin(triggerPin) == 0:
                # 检测按键,如果按键按下,启动相机拍照
                print("no triggle, waiting...")
                time.sleep(0.2)
            else:
                # 开启继电器和灯管
                piGPIO.setPin(fanPin)
                piGPIO.setPin(lightPin)
                # 启动tGUI
                global triggerFlag
                triggerFlag = True
                print("Triggled! Waiting for camera respond...")
                # 启动相机拍照并生成二维码
                generateQRCode.generateQR(runCamera.runCameraAndTakePhotoAndUpload())
                os.system('python thermal_print.py')
                # 关闭继电器和灯管
                piGPIO.resetPin(fanPin)
                piGPIO.resetPin(lightPin)
                # 延迟下次触发的时间
                time.sleep(3)

# 线程_rGUI
class thread_rGUI(myThread):
    def run(self):
        rGUI.run_Self()

# 线程Debug用
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

# 线程锁
threadLock = threading.Lock()
threads = []

# 创建线程
thread1 = thread_pinDetective(1, "Thread-Pin", 1)
thread2 = myThread(2, "Thread-resultGUI", 1)

# 开启线程
thread1.start()
thread2.start()

# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)

# 等待所有线程完成
for t in threads:
    t.join()
print("退出主线程")

