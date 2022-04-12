# AutoReportWin
## 使用方法
下载并安装Chrome

编辑config.ini，设置正确的账号密码。

运行onserver.py

## 修改chromedriver

为使脚本正确运行，请保证chrome版本与路径中的chromedriver.exe版本吻合。自带的ChromeDriver版本为100.0.4896.60。[ChromeDriver下载](https://chromedriver.chromium.org/downloads)

将onserver.py文件中的DRIVER_PATH常量修改为chomedriver.exe的路径。

默认在根目录下寻找chromedriver.exe
