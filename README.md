# httprunner_proxy
接口抓包生成httprunner可执行yaml格式的工具


## 项目使用到的开源工具

1. mock服务，[doo](https://sweeter.io/#/doo/)
2. 抓包服务，[mitmproxy](https://docs.mitmproxy.org/stable/)
3. 测试框架，[httprunner](https://cn.httprunner.org/)

## 项目使用方法

1. 配置环境变量 TEST_HOST，TEST_NAME，PROXY_PORT，其中TEST_HOST必须配置为`http://ip:port`的格式，TEST_NAME是当前录制的测试集前缀，PROXY_PORT是抓包接口

   注意：`本地起动的服务，若抓取postman发出的请求可直接调用接口，若抓取通过前端服务发出的请求，前端服务的后端服务调用地址和环境变量都需要配置为本机ip`
2. 配置本地代理，代理地址默认127.0.0.1:8080，  proxy目录下运行```pipenv run mitmdump -s catch.py```启动代理服务，可以通过增加`-p` 参数修改默认端口，.env中的PROXY_PORT配置需要和启动的端口配置一致
   如果是第一次使用mitmproxy，启动抓包后需要访问`http://mitm.it/`,如果出现证书下载界面则启动成功，下载证书安装后可以正式开始使用
3. mock目录下，运行```pipenv run python3 app.py example.yml```启动mock服务
4. 使用postman发出请求

post接口：
```
url:http://127.0.0.1:5000/api/authentication/login
method: post
body:{
    "account":"admin",
    "password": "123456"
}
```
get接口：
```
url:hhttp://127.0.0.1:5000/api/news?id=10001
method: get
```
5. api、testcase、testsuit目录下可以看到已经生成了相关接口的配置文件

   其中singleinterface目录下是单独接口的testcase数据，同时会按照当前的接口调用顺序生成teststeps流程一致的testcase文件

   testsuites也会生成调用二者的suit
6. 关闭代理服务并取消代理，开始进行接口测试（也可以不关，不过建议关闭
7. 使用 ```pipenv run hrun testsuites/xxx_testsuite.yml``` 命令运行测试文件（部分用法也可使用demo文件体验）
8. 之后可以在reports目录下使用open命令打开测试报告