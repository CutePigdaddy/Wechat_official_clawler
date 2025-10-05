import sqlite3
import os
from datetime import datetime


def create_db(DB,table_name,fields):
  #---建表---#
  """
    create_db介绍
    用途:用于创建在'DB.db'数据库的一个名为table_name的表
    参数:
      DB:数据库文件名
      table_name:表名
      fields:字段定义字典，如 {"id": "INTEGER PRIMARY KEY","name": "TEXT"}
  """
  conn = sqlite3.connect(f"{DB}.db")
  c = conn.cursor()
  field_defs = ', '.join([f"{name} {type_}" for name,type_ in fields.items()])
  c.execute(f"""
  CREATE TABLE IF NOT EXISTS {table_name}({field_defs})
  """)
  conn.commit()
  conn.close()


def insert_db(DB,table_name,data):
  """
    insert_db介绍
    用途:用于往DB.db文件中的table_name表插入data数据
    参数:
      DB:数据库文件名
      table_name:表名称
      data:字典形式，字典的键要跟数据库表的字段一样(可少不可多)
  """
  conn = sqlite3.connect(f"{DB}.db")
  c = conn.cursor()
  #---从data中抓出key来进行插入---#
  keys = ", ".join(data.keys())
  placeholders = ", ".join(f":{k}" for k in data.keys())
  try:
    c.execute(f"""
      INSERT INTO {table_name}({keys}) 
      VALUES ({placeholders})
      """
      ,data
    )
    conn.commit()
    print(f"插入[{data["name"]}]成功！")
  except sqlite3.IntegrityError:
    print("😨已存在，跳过插入")
  conn.close()


def search_db(DB,table_name,field,tag):
  """
    search_db介绍
    用途:用于往DB文件中的table_name表针对field字段搜索tag关键词相关记录,并返回一个sqlite3.Row对象的列表,可以用result = [dict(row) for row in rows]转换
    特别地，想要拿所有数据的话,tag处留空字符串就可以了
    参数:
      DB:数据库文件名
      table_name:数据库中表的名称
      field:字段名称
      tag:关键词
  """
  conn = sqlite3.connect(f"{DB}.db")
  conn.row_factory = sqlite3.Row
  c = conn.cursor()

  #---查询数据---#
  like_param = f"%{tag}%"
  c.execute(f"""
    SELECT *
    FROM {table_name}
    WHERE {field} LIKE ?
  """,(like_param,))

  #---输出数据---#
  rows = c.fetchall()
  conn.close()
  if rows:
    print(f"找到{len(rows)}条相关记录")
    return rows
  else:
    print("查找不到!")  
    return []


def delete_db(DB,table_name,record_id):
  """
    delete_db介绍
    用途:用于DB文件中的table_name表删除record_id所在记录
    参数:
      DB:数据库文件名
      table_name:数据库中表的名称
      id:记录的id
  """
  conn = sqlite3.connect(f"{DB}.db")
  c = conn.cursor()

  name = c.execute(f"""
    SELECT name FROM {table_name}
    WHERE id = ?
  """,(record_id,)).fetchone()[0]
  c.execute(f"""
    DELETE FROM {table_name} 
    WHERE id = ?
  """,(record_id,))
  conn.commit()

  #c.rowcount 说明c是否对行有影响#
  if c.rowcount > 0 :
    print(f"已经删除id:[{record_id}]|name:[{name}]的记录！🫡")
  else:
    print(f"找不到id为[{record_id}]|name:[{name}]的记录！🥹")
  conn.close()



