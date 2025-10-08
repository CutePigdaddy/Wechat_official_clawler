from fetch_tools import *
#https://mp.weixin.qq.com/s/xI3JMqEZqJXDCnxjCDR4Fg 测试用
if __name__ == "__main__":
  method = input("输入1：获得公众号主页/获取单篇文章内容\n" \
  "输入2：获取公众号下的文章列表\n")
  if method == "1": 
    fetch_accounts(input("请输入你想要的公众号主页的一篇文章短链:"))
  if method == "2": 
    #初始化session、headers
    headers_text = ""
    print("请输入你的headers（多行，输入END结束）：")
    while True:
      line = input()
      if line.strip() == "END":
        break
      headers_text += line + "\n"
    form_headers(headers_text)
    data,r = fetch_article_list(input("请输入你获取到的完整getmsg链接:"),timeout = 50)
    if data is not None:
      with open("data.json","w",encoding="utf-8") as f:
       json.dump(data,f,ensure_ascii=False,indent=2)
    with open("r.txt","w",encoding='utf-8') as f:
      f.write(r.text)
  
  articles = data["general_msg_list"]
  urls = re.findall(r'content_url\":\"(.*?)\"',articles)
  titles = re.findall(r'\"title\":\"(.*?)\"',articles)

  #建文件夹
  text = ""
  for url,title in zip(urls,titles):
    path_name = 'Result.txt'
    text = text + "\n" + f"{title}→{url}"
  with open(path_name,"w",encoding='utf-8') as f:
    f.write(text)
  print("获取成功，已保存到Result.txt")
#with open("test.txt","w",encoding='utf-8') as f:
#  f.write(s.get("http://mp.weixin.qq.com/s?__biz=MzAxODAzMjQ1NQ==&amp;mid=2707720384&amp;idx=1&amp;sn=6dfc4e73022f4aa332835b0cf673f71e&amp;chksm=be71d26607dea4a8e39afd1ea24547402afb6fa0168fa00e42e04415b83724e603af90ad083a&amp;scene=27#wechat_redirect",headers=article_headers,verify=False).text)




