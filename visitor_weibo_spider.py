from login import get_session
from login.cookies_gen import get_cookies
from utils import FakeChromeUA
import requests
from lxml import etree
import re
import json

def parse_url(url):
    cookies = get_cookies()
    headers = {
        'User-Agent': FakeChromeUA.get_ua(),
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    response = requests.get(url,cookies=cookies,headers=headers,verify=False)
    return response

def get_content_list(response):
    ret = re.findall(r"<script>FM\.view\((.*?)\)</script>", response.content.decode())
    for i in ret:
        json_data = json.loads(i)
        if json_data["ns"] == "pl.content.signInPeople.index":
            break
    # with open("json.html","w",encoding="utf-8") as f:
    #     f.write(json_data["html"])
    html = etree.HTML(json_data["html"])
    li_list = html.xpath("//ul[@class='follow_list']/li")
    for li in li_list:
        print("微博名字:", li.xpath(".//div[@class='info_name W_fb W_f14']//strong/text()")[0])


if __name__ == '__main__':
    url ="https://d.weibo.com/1087030002_2975_1003_0?page=1"
    response = parse_url(url)
    get_content_list(response)

