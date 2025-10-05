from db_operations import *
import json

DB = "TEST"
table_name = "accounts"
field={
  "id":"INTEGER PRIMARY KEY",
  "name":"TEXT",
  "url":"TEXT",
  "last_checked":"TEXT",
  "tag":"TEXT"
}
rows = search_db(DB,table_name,"id","")
results = [dict(row) for row in rows]
if not results:
  print("啥都没有😨")
else:
  print("查找完毕，准备输出😘")
  with open("result.txt","w",encoding="utf-8") as f:  
    for result in results:
      f.write("|".join(f"{k}={v}" for k,v in result.items()) + "\n")
  print("已输出文件，请查收哦👍")
