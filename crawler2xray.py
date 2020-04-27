#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org
# time:2020/4/27
# wget https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/706915/chrome-linux.zip
# wget https://github.com/0Kee-Team/crawlergo/releases/download/v0.2.0/crawlergo_linux_amd64.zip
# apt-get install -yq --no-install-recommends      libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3      libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4      libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1      libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 libnss3
# wget https://github.com/chaitin/xray/releases/download/0.20.0/xray_linux_amd64.zip
# 1.xray webscan --listen 127.0.0.1:7777 --html-output test.html
# 2.py -2 crawer2xray.py -u http://testphp.vulnweb.com/ [-F targets.txt]
import Queue
import json
import threading
import subprocess
import requests
import optparse
import sys
import warnings
import time
warnings.filterwarnings(action='ignore')


chrome_path =''
threads = 2
tclose = 0

def put_file_contents(filename,contents):
    with open(filename,"ab+") as fin:
        fin.write(contents+"\n")

def get_file_content(filename):
    result = []
    f = open(filename, "r")
    for line in f.readlines():
        result.append(line.strip())
    f.close()
    return result


class Producer(threading.Thread):

    def __init__(self, t_name, urls,queue):  # 传入线程名、实例化队列
        threading.Thread.__init__(self, name=t_name)  # t_name即是threadName
        self.data = queue
        self.urls = urls

    def run(self):
        global threads, chrome_path,tclose
        urls = self.urls
        for url in urls:
            print("Start Crawer %s."%(url))
            target = url
            try:
                cmd = [r"./crawlergo/crawlergo", "-c", chrome_path, "-t", "{0}".format(threads), "-f",
                       "smart", "--fuzz-path", "--output-mode", "json", target]
                rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = rsp.communicate()
                result = json.loads(output.decode().split("--[Mission Complete]--")[1])
            except Exception as e:
                print(e.message)
                continue
            req_list = result["req_list"]
            for req in req_list:
                self.data.put(req)
            log = "[%s crawler finished ]."%(url)
            print("Total requests numbers is %s"%(self.data.qsize()))
            put_file_contents('crawlog.txt', log)
        print("%s: %s producing finished!" % (time.ctime(), self.getName))
        tclose = 1
        return


class Consumer(threading.Thread):

    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def task(self,req):
        proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777',
        }
        urls0 =req['url']
        headers0 =req['headers']
        method0=req['method']
        data0=req['data']
        try:
            if(method0=='GET'):
                requests.get(urls0, headers=headers0, proxies=proxies,timeout=30,verify=False)
            elif(method0=='POST'):
                requests.post(urls0, headers=headers0,data=data0, proxies=proxies,timeout=30,verify=False)
        except Exception as e:
            print(e.message)
        return

    def run(self):
        global  tclose
        print("Start doing task.")
        print("Current Scan Task num is %d." % (self.data.qsize()))
        while True:
            try:
                task_num = self.data.qsize()
                if task_num > 0:
                    print("Current Scan Task num is %d." % (task_num))
                    req = self.data.get()
                    self.task(req)
            except Exception as e:
                print(e.message)
            if task_num == 0 and tclose == 1:
                time.sleep(10)
                break
        print("%s: %s consuming finished!" % (time.ctime(), self.getName()))
        return


def main():
    commandList = optparse.OptionParser('usage: %prog [-u url -f urls.txt]\nIf use xray set --listen 127.0.0.1:7777')
    commandList.add_option('-f', '--file', action='store',
                           help='Insert filename of stored urls ::')
    commandList.add_option('-u', '--url', action="store",
                           help="Insert TARGET URL: http[s]://www.victim.com[:PORT]",
                           )
    commandList.add_option('-t', '--threads', action="store", default=6, type="int",
                           help="set scan thread number.default vaule is 6")
    commandList.add_option('--path', action="store", default="./chrome/chrome",
                           help="set chrome path.",
                           )
    options, remainder = commandList.parse_args()
    if (not options.file) and (not options.url):
        commandList.print_help()
        sys.exit(1)
    urls = [options.url] if options.url else get_file_content(options.file)
    global  threads,chrome_path
    threads = options.threads
    chrome_path = options.path
    print("%s: start main." % (time.ctime()))
    queue = Queue.Queue()  # 队列实例化
    producer = Producer('Pro.',urls,queue)  # 调用对象，并传如参数线程名、实例化队列
    consumer = Consumer('Con.', queue)  # 同上，在制造的同时进行消费
    producer.start()  # 开始制造
    consumer.start()  # 开始消费

    producer.join()
    consumer.join()
    print('All threads terminate!')


if __name__ == '__main__':
    main()

