import os
import oss2
import tGUI

# 配置OSS
auth = oss2.Auth('yourAccessKeyId', 'yourAccessKeySecret')
bucket = oss2.Bucket(auth, 'http://oss-cn-shenzhen.aliyuncs.com', 'yourBucketName')

def runCameraAndTakePhotoAndUpload():
    print("run time count GUI")
    tGUI.run_self()
    # 启动相机
    print("camera run")
    os.system('raspistill -f -t 1000 -o test.jpg -w 1280 -h 768')
    print("camera shot done")
    # 上传照片toOSS
    return uploadPhoto()


def uploadPhoto():
    # 读取图片
    with open('test.jpg', 'rb') as fileobj:
        # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
        fileobj.seek(0, os.SEEK_SET)
        # Tell方法用于返回当前位置。
        current = fileobj.tell()
        print("uploading image...")
        bucket.put_object('raspiInteractiveCameraDemo/test.jpg', fileobj)
        print("uploading done!")
    # 返回对应的访问URL,600s内有效
    imgUrl = bucket.sign_url('GET', 'raspiInteractiveCameraDemo/test.jpg', 600)
    print("The url of that image is :" + imgUrl)
    return imgUrl
