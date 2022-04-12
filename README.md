# AutoReportWin
auto report
## 使用方法
下载并安装Chrome

编辑config.ini，设置正确的账号密码。

如不需使用ALIAS和MAIL属性，请将值设为0。

运行onserver.py

## 修改chromedriver

为使脚本正确运行，请保证chrome版本与路径中的chromedriver.exe版本吻合。自带的ChromeDriver版本为100.0.4896.60。[ChromeDriver下载](https://chromedriver.chromium.org/downloads)

将onserver.py文件中的DRIVER_PATH常量修改为chomedriver.exe的路径。

默认在根目录下寻找chromedriver.exe

## 自动反馈

编辑autoReport.py，修改代码开头的常量，进行结果反馈。

同时，可以在config.ini中修改ALIAS和MAIL的值，向个人发送填报结果。

目前有三种反馈方式，开启与关闭可以在onserver.py中调整

## 环境要求
Python3

pip 见requirements.txt
