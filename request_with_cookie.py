#!/usr/bin/python3
# coding: utf-8

import simplejson
import subprocess
"""
    添加Cookie扫描示例
    
    命令行调用时：
    ./crawlergo -c /home/test/chrome-linux/chrome -o json --ignore-url-keywords quit,exit,zhuxiao --custom-headers "{\"Cookie\": \"crawlergo=Cool\"}"

    使用 --ignore-url-keywords 添加你想要的排除的关键字，避免访问注销请求
"""


def main():
    target = "http://test.com/iWebShop5.6/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/74.0.3945.0 Safari/537.36",
        "Cookie": "lastUrl=%2FiWebShop5.6%2Findex.php%3Fcontroller%3Dmember%26action%3Dseller_list; __atuvc=2%7C7; cookieconsent_status=dismiss; Hm_lvt_f6f37dc3416ca514857b78d0b158037e=1585477788; Hm_lpvt_f6f37dc3416ca514857b78d0b158037e=1585477788; PHPSESSID=87lfdt8o6r23jva61h29qb8rp3; iweb_callback=59c751b6344a09b2d3UgICBgBUAFIGVFVUUVEBBwBUW1MDAgUGBwcGBVZXUlI; iweb_user_id=da2dae43a98d9c588aUgVVBlRWA1IEUlAABlpUDgMBAV8CBlFRBV9cU1BWU1YJ; iweb_username=f0ddda1dcf9d189e23AlFWBQMAUVYBAFIMUgJfVwkECFZUDAVXBg8BUF0HBFFCVkAV; iweb_user_pwd=76a55b82ba902339deAVNWAggGVFZUCQZSUVBSBwpRBgNVCQ5RUARTAFZTB1IAAANTBwUBXABdBAAGAVdVVwQDDwMFBVMHCwcCXVoBVA; iweb_head_ico=dd0f50cf45519d8678VVQAAFMFB1EAB1FVVlQDCAxVDwpbCl8LVwYJAAoCA1YURFVcAFBKE0ABQzleVFcYAFVXDQkBUwwBUAMAVgIPAVlPFApe; iweb_last_login=d149e6d8e02ba763c7BgEHUwNRBFEEVFJUUgNUB1YFUAVWAAUBDVUHVAwEA1BQBAUIFVUCFAVdQwcEC1ELAgFT; iweb_captcha=e5c0da1829e2346f6bVFIFCAdVAQVUUVdZA1cEVQAHUAUBVwMKAAVXB1YOAV1OWVhbUA; iweb_admin_role_name=b3c1972894c6978353AAIFUVNSB1MGA1wPWQFbDlMBVwAGAQEBWgYPBwdTAQeLh7aDiJXVn5KCoLTSqag; iweb_admin_id=72bf2a52738ea25862VAJUBwABUVNUVQZRVloCBV8GDFFVBFEFDgddBwJRU1YF; iweb_admin_name=cde789b2c16562672eCAgHBAhSAwNSAQRUAgUABVANA15SD1NWDgAGWlJXAg5ZXFlYCw; iweb_admin_pwd=0a82c691d9323676ceU1QHAAFTAFYJUwVUAwUGV1IBAVUCUVtaXlBVW1FWAAUDXwEFBAIOBQcBDlFaB10AAFsEUFdbAwxcVwEBB1NWVg; iweb_lastInfo=e74b4e2e6dffcd7cceVgkCAQEBVQMHAgBQA1cFUwwGVQZTVlYAUlBWUQlQBAAdCwZbUAAWH1VTDFBXFj4OC0NE; iweb_seller_id=fe5f5c59903d0193dcBANRAlZVVAIDAARRUgdQV1sDDwMAUwUCUARaUQ4ADlZR; iweb_seller_name=4c66276cdda034536bVgJSBwcFUgBUVgZZBF0EA1UEUgMCB1cEUQFTVwlWXFdQXU4; iweb_seller_pwd=6f178fff18dd5e584aCQBSUVYHVgFRBwVZUFdaAQUAVAUHAgBVCARUXFFWVwUHXgECUgcDVAwFCAMMVgUGBlVUUFNdBQAMW1AHUwECBw"
    }
    cmd = [r"D:/Tools/PTTools/VulnScan/crawlergo_windows_amd64/crawlergo.exe", "-c", "D:/Tools/PTTools/VulnScan/chrome-win/chrome.exe",
           "-o", "json", "--ignore-url-keywords", "quit,exit,zhuxiao,logout", "--custom-headers", simplejson.dumps(headers),
           target]

    rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = rsp.communicate()

    result = simplejson.loads(output.decode().split("--[Mission Complete]--")[1])
    req_list = result["req_list"]
    for each in req_list:
        print(each)


if __name__ == '__main__':
    main()





