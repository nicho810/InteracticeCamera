import oss2

# 配置OSS
auth = oss2.Auth('yourAccessKeyId', 'yourAccessKeySecret') 
bucket = oss2.Bucket(auth, 'http://oss-cn-shenzhen.aliyuncs.com', 'yourBucketName') 


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    if method == 'GET' and path == '/':
        imgUrl = bucket.sign_url('GET', 'raspiInteractiveCameraDemo/test.jpg', 6000)
        # print("The url of that image is :" + imgUrl)
        return_url = "<img src=\"" + imgUrl + "\" />"
        return_url = bytes(return_url, encoding="utf8")
        # print(return_url)
        return_list = ["", ""]
        return_list[0] = [
            b'hello']
        return_list[1] = [return_url]
        return return_list[1]


from wsgiref.simple_server import make_server

# 创建一个服务器，IP地址为空，端口是8999
httpd = make_server('', 8999, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()
