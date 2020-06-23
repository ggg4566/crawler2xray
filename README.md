# crawler2xray
[![Python 2.7](https://img.shields.io/badge/python-2.7-yellow.svg)](https://www.python.org/)[![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://github.com/ggg4566/PocStart/blob/master/LICENSE)

结合[**360 0Kee-Team/crawlergo**](https://github.com/0Kee-Team/crawlergo)爬虫和[**长亭科技/xray**](https://github.com/chaitin/xray)被动扫描器自动寻找漏洞。可以通过输入目标文件作为参数进行自动化批量扫描，相同的功能已经有人实现过了[【crawlergo_x_xray】](https://github.com/timwhitez/crawlergo_x_XRAY)不过可用性并不是很友好，linux vps测试没有问题，本地windows python3.6环境测试的时候发现爬虫并没有爬到足够多的数据，调了半天不知道原因，自己动手丰衣足食，最后用python2重新造了一个轮子。

**脚本：**

---

|序号|脚本名称|描述|
|:---:|:---|:---|
|1|crawler2xray.py|主文件|
|2|crawlergo2xray.py|基于crawlergo_x_xray修改而来(python3)|

**用法：**

---

```
Usage: crawler2xray.py [-u url -f urls.txt]
If use xray set --listen 127.0.0.1:7777

Options:
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  Insert filename of stored urls ::
  -u URL, --url=URL     Insert TARGET URL: http[s]://www.victim.com[:PORT]
  -t THREADS, --threads=THREADS
                        set scan thread number.default vaule is 6
  --path=PATH           set chrome path.

```

1. 开启xray

   ./xray_linux_amd64 webscan --listen 127.0.0.1:7777 --html-output test.html

2. python2 crawler2xray.py -u http://testphp.vulnweb.com/

   ```
   python2 crawler2xray.py -u http://testphp.vulnweb.com/
   Mon Apr 27 02:37:00 2020: start main.
   Start Crawer http://testphp.vulnweb.com/.
   Start doing task.
   Current Scan Task num is 0.
   Total requests numbers is 54
   Mon Apr 27 02:37:59 2020: <bound method Producer.getName of <Producer(Pro., started 139654939461376)>> producing finished!
   Current Scan Task num is 54.
   Current Scan Task num is 53.
   Current Scan Task num is 52.
   ...
   Current Scan Task num is 1.
   Mon Apr 27 02:38:19 2020: Con. consuming finished!
   All threads terminate!
   ```

   

**部署：**

---

* 克隆工程git clone https://github.com/ggg4566/crawler2xray
* 下载crawlergo 存放在项目路径crawlergo下
* 下 载chrome  存放在项目路径chrome下
* 下载部署xray

```
Ubuntu 16.04.3 install cmd.
# git clone https://github.com/ggg4566/crawler2xray
# wget https://github.com/0Kee-Team/crawlergo/releases/download/v0.2.0/crawlergo_linux_amd64.zip
# unzip crawlergo_linux_amd64.zip
# mv crawlergo_linux_amd64/crawlergo_linux_amd64 crawler2xray/crawlergo
# wget https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/706915/chrome-linux.zip
# unzip chrome-linux.zip
# mv chrome-linux/* crawler2xray/chrome
# apt-get install -yq --no-install-recommends      libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3      libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4      libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1      libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 libnss3
```

**参考：**

---

https://xz.aliyun.com/t/7047
