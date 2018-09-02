# 互动拍照墙 | Interactive camera
> 通过触发装置,启动风扇,在倒计时结束和头发飘飘的时候留下精彩的一瞬间,照片同时上传到阿里云OSS储存,拍照结束后可打印小票(附有拍照评分和照片下载二维码)
---
### 硬件
1. 树莓派(Raspberry Pi 3B/3B+)
2. RPi Camera (G)
3. 嵌入式热敏打印机Embedded Thermal Printer
4. 继电器模块(Grove-Relay)
5. 按键模块(Grove-Button)

### 配置树莓派
1. 下载树莓派镜像,使用ether等烧录镜像,并连接显示器鼠标键盘进行初始化配置,连接网络(wifi)
```
https://www.raspberrypi.org/downloads
```
2. 开启camera和serial(顺便开启vnc和ssh)
```
# 终端运行以下指令
sudo raspi-config
# 选择5 Interface Option
# 选择P1 Camera ,然后选择Enable
# 选择P2 SSH ,然后选择Enable
# 选择P3 VNC ,然后选择Enable
# 选择P6 Seria,第一步选择NO,第二部选择YES
# Finish
# 重启树莓派
sudo reboot now
```
3. 连接相机模块和按键继电器以及热敏打印机**(这里按照物理引脚为准)**
```
triggerPin = 16  # 拍照触发按键
fanPin = 18      # 风扇输出
lightPin = 22    # 灯输出
#热敏打印机串口TX --> 树莓派RX(10)
#热敏打印机串口RX --> 树莓派TX(8)
#连接完成后可以进行测试(相机模块安装后需要重启才能识别,建议关机状态下安装)
```
4. 相机测试
```
# 在终端运行
raspistill -f -t 1000 -o test.jpg -w 1280 -h 768
# 代码含义:
# -->拍摄静态图片,打开预览窗口,倒计时一秒,保存为test.jpg,照片宽度为1280,高度为768
# 之后可根据自己的需要酌情更改,之后会在python3中调用os模块执行这段指令
```
5. 安装python模块
```
# 在终端运行
# 因为这里使用python3,所以使用pip3安装
pip3 install oss2 #阿里云OSS
pip3 install guizero #图形界面库
pip3 install qrcode #二维码库
```
6. 注册阿里云OSS储存服务,新建bucket,获取AccessKeyId,AccessKeySecret
```
# -*- coding: utf-8 -*-
# OSS测试代码
import oss2
# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', '<yourBucketName>')
# 必须以二进制的方式打开文件，因为需要知道文件包含的字节数。
with open('<yourLocalFile>', 'rb') as fileobj:
    # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
    fileobj.seek(1000, os.SEEK_SET)
    # Tell方法用于返回当前位置。
    current = fileobj.tell()
    bucket.put_object('<yourObjectName>', fileobj)
# 详情参考 https://help.aliyun.com/document_detail/88426.html?spm=a2c4g.11186623.6.733.31cc6beeKRYbEc
```

### 配置客户端代码
1. 下载代码
```
# 在终端运行以下代码
cd ~
git clone https://github.com/nicho810/InteracticeCamera.git
cd InteracticeCamera
```
2. 填写阿里云OSS API key
```
cd ~/InteracticeCamera/client
sudo nano runCamera.py
```
将下面代码中的yourAccessKeyId;yourAccessKeySecret;yourBucketName,以及服务器地址改成你的
```
auth = oss2.Auth('yourAccessKeyId', 'yourAccessKeySecret')
bucket = oss2.Bucket(auth, 'http://oss-cn-shenzhen.aliyuncs.com', 'yourBucketName')
```
> 使用Ctrl+o保存;Ctrl+x退出

3. 运行代码测试
```
cd ~
python3 InteracticeCamera/client/main_demo.py
```

4. 可选方式
```
# 先运行背景GUI
cd ~
python3 InteracticeCamera/client/rGUI.py
# 该代码会以全屏的方式运行,再使用快捷键打开另一个终端,运行以下代码
cd ~
python3 InteracticeCamera/client/main_demo.py
```

### 配置服务端代码(可选)

1. 使用一个有公网IP的服务器,运行以下代码(python3)
```
cd ~
git clone https://github.com/nicho810/InteracticeCamera.git
cd InteracticeCamera/server
sudo nano run_server.py
# 讲代码中的yourAccessKeyId;yourAccessKeySecret;yourBucketName,以及服务器地址改成你的
```
> 使用Ctrl+o保存;Ctrl+x退出
2. 运行代码
```
cd ~/InteracticeCamera/server
python3 run_server.py
```
3. 打开浏览器,输入http://你的服务器域名或者ip地址:8999
> 在浏览器中将显示最新上传的图片,将这段完整网址(包括后面的端口名)生成二维码,在使用取模软件生成点阵数据,替换热敏打印机打印代码中的数据,详情参考:  ~/InteracticeCamera/client/Python-Thermal-Printer/printertest.py
