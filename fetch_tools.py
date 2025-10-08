import requests
import json
from bs4 import BeautifulSoup
import re
import json
import os
from playwright.sync_api import sync_playwright

#HEADERS需要抓包获取
s = requests.Session()
headers = {}
default_headers = {
  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541022) XWEB/16467 Flue",
  "Referer":"https://mp.weixin.qq.com/mp/"
}
def form_headers(headers_text):
  """
  功能：输入text版本的headers自动转化为字典headers
  :param headers_text:在Fiddler里面找到mp.weixin.qq.com后面带有getmsg（没有的话在主页往下拉让他刷新）的请求，找到右边的headers，右键复制所有headers，把前面一段GET...一大段URL删掉，保留下面的headers
  :return:返回一个headers Dict数据
  例如：
        Host: mp.weixin.qq.com
        Connection: keep-alive
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 NetType/WIFI        MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541022) XWEB/16467 Flue
        X-Requested-With: XMLHttpRequest
        Accept: */*
        Sec-Fetch-Site: same-origin
        Sec-Fetch-Mode: cors
        Sec-Fetch-Dest: empty
        Referer: https://mp.weixin.qq.com/mp/profile_ext?....
        Accept-Encoding: gzip, deflate, br
        Accept-Language: zh-CN,zh;q=0.9
        Cookie: ......

  """
  for line in headers_text.splitlines():
      line = line.strip()
      if not line or ":" not in line:
          continue  # 跳过空行或无冒号行
      key, value = line.split(":", 1)
      headers[key.strip()] = value.strip()
  s.headers.update(headers)
  print("Headers配置成功！")
  return headers

def fetch_accounts(article_url):
  """
  功能：通过某个文章短链获取公众号主页的URL, 并输出提示
  :param article_url:微信公众号文章的短链，一定得是短链哦
  """
  print(headers)
  document = fetch_article_details(article_url,10)
  account_url = f"https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={document["biz"]}&scene=124#wechat_redirect"
  print(f"成功获取公众号主页URL→{account_url}")
  print("可以复制到微信文件传输助手，然后通过微信客户端打开！")

def fetch_article_details(url,timeout):
  """
  功能：输入公众号文章URL，可以获取文章作者、标题等
  :param url: 公众号文章url
  :param timeout: 获取间隔
  :return: Dict数据，有"status","content","title","author","create_time","biz"，status为1的时候成功，为0的时候失败
  """
  url = url.strip() #去除头尾空格换行

  print("-----开始请求-----")
  resp = s.get(url,headers=default_headers,timeout=timeout,allow_redirects=True,verify=False)
  if resp.status_code == 200:
    print("√√√√√请求成功！√√√√√")
  else:
    print("×××××请求失败🥹×××××")
    return {"status":0}
  resp.encoding = resp.apparent_encoding
  status = re.search("当前环境异常，完成验证后即可继续访问",resp.text)
  if status:
    print("!!!!!环境异常,程序执行失败!!!!!!")
    return {}
  html = resp.text
  soup = BeautifulSoup(html,"lxml")
  print("-----开始搜索元素-----")
  content = soup.find("div",class_ = "rich_media_content").get_text("\n",strip=True)
  if content:
    print("成功找到文章内容！")
    print(content[:10]+"...")
  title = soup.find("h1",{"class":"rich_media_title","id":"activity-name"}).get_text(strip=True)
  if title:
    print("成功找到文章标题！")
    print(f"[Title]→{title}")
  author = soup.find("a",{"id":"js_name"}).get_text(strip=True)
  if author:
    print("成功找到文章作者！")
    print(f"[Author]→{author}")
  biz = re.search(r'var biz\s*=\s*"(.*?)";',html).group(1).replace('" || "','').replace('"','')
  if biz:
    print("成功获取公众号链接！")
    print(f"[Official]→https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={biz}&scene=124#wechat_redirect")
  create_time = re.search(r"var createTime = '(.*?)';",html).group(1)
  if create_time:
    print("成功获取文章创建时间！")
    print(f"CreateTime→{create_time}")
  os.makedirs("HTML",exist_ok=True)
  os.makedirs("Articles",exist_ok=True)
  file_name = re.sub(r'[\\/:*?"<>|]', "_", f"{author}-{title}-{create_time}.html")
  html_path = os.path.join("HTML",file_name)
  print(f"HTML长度: {len(html)}")
  print(f"文章内容长度: {len(content)}")
  print("-----开始保存HTML源码到本地-----")
  with open(html_path,"w",encoding="utf-8") as f:
    f.write(html)
  print("-----成功保存HTML源码到本地-----")
  file_name = re.sub(r'[\\/:*?"<>|]', "_", f"{author}-{title}-{create_time}.txt")
  txt_path = os.path.join("Articles",file_name)
  print("-----开始保存文章文本到本地-----")
  with open(txt_path,"w",encoding="utf-8") as f:
    f.write(content)
  print("-----成功保存文章文本到本地-----")
  return {"status":1,"content":content,"title":title,"author":author,"create_time":create_time,"biz":biz}

def fetch_article_list(url,timeout):
  """
  功能：通过完整的公众号主页getmsgURL获取文章列表
  :param url:完整URL,
  :param timeout:获取间隔,
  :return:Json数据,原始返回数据
  """
  resp = s.get(url,timeout=timeout)
  try:
    data = resp.json()
    return data,resp
  except Exception:
    print("没有获取到文章！")
    return None,resp

