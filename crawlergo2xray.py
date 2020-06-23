#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org
# time:2020/4/21
# refer:https://xz.aliyun.com/t/7047
# 1. xray_linux_amd64 webscan --listen 127.0.0.1:7777 --html-output test.html
# 2 python3 crawlergo2xray -u http://testphp.vulnweb.com/
import queue
import json
import threading
import subprocess
import requests
import optparse
import sys
import warnings
warnings.filterwarnings(action='ignore')

urls_queue = queue.Queue()
tclose=0
path = "D:/Tools/PTTools/VulnScan/chrome-win/chrome.exe"
def put_file_contents(filename,contents):
    with open(filename,"a+") as fin:
        fin.write(contents+"\n")


def get_file_content(filename):
    result = []
    f = open(filename, "r")
    for line in f.readlines():
        result.append(line.strip())
    f.close()
    return result


def check_target(target):
    if not "http" in target.strip():
        target = ""
    return target


def request0():
    global tclose
    while tclose==0 or urls_queue.empty() == False:
        if(urls_queue.qsize()==0):
            continue
        print(urls_queue.qsize())
        req =urls_queue.get()
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
        except:
            continue
    return


def craw_url(url,threads,path):
    target = url
    try:
        cmd = ["./crawlergo", "-c", path, "-t", "{0}".format(threads), "-f",
               "smart", "--fuzz-path", "--output-mode", "json", target]
        rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = rsp.communicate()
        result = json.loads(output.decode().split("--[Mission Complete]--")[1])
    except:
        return
    req_list = result["req_list"]
    log = "{0}[crawl ok].\n".format(url)
    print(log)
    put_file_contents('crawlog.txt',log)
    for req in req_list:
        urls_queue.put(req)
    print("[scanning]")


def main():
    commandList = optparse.OptionParser('usage: %prog [-u url -f urls.txt]\nIf use xray set --listen 127.0.0.1:7777')
    commandList.add_option('-f', '--file', action='store',
                           help='Insert filename of stored urls ::')
    commandList.add_option('-u', '--url', action="store",
              help="Insert TARGET URL: http[s]://www.victim.com[:PORT]",
            )
    commandList.add_option('-t', '--threads', action="store", default = 6,type="int",
                  help="set scan thread number.default vaule is 6")
    commandList.add_option('--path', action="store",default = "./chrome/chrome",
              help="set chrome path.",
            )
    options, remainder = commandList.parse_args()
    if (not options.file) and (not options.url):
        commandList.print_help()
        sys.exit(1)
    urls = [options.url] if options.url else get_file_content(options.file)
    threads = options.threads
    path = options.path
    t = threading.Thread(target=request0)
    t.start()
    for url in urls:
        url = check_target(url)
        if url:
            craw_url(url,threads,path)
    global tclose
    tclose = 1
    print("Finshed Crawler!!!\n")


if __name__ == '__main__':
    main()
