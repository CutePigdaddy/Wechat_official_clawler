from db_operations import *
import json
from datetime import datetime,timedelta
import random

DB = "TEST"
table_name = "accounts"
"""
field={
  "id":"INTEGER PRIMARY KEY",
  "name":"TEXT",
  "url":"TEXT",
  "last_checked":"TEXT",
  "tag":"TEXT"
}

create_db(DB,table_name,field)
"""
tags = ["教育", "科技", "生活", "财经", "娱乐"]
for i in range(1, 100):
  acc = {
      "id": i,
      "name": f"公众号{i}",
      "url": f"https://mp.weixin.qq.com/s/{random.randint(100000,999999)}",
      "last_checked": (datetime.utcnow() - timedelta(days=random.randint(0, 30))).isoformat(),
      "tag": random.choice(tags)
  }
  insert_db(DB,table_name,acc)