from db_operations import *
DB = "TEST"
table_name = "accounts"

for i in range(1,100):
  delete_db(DB,table_name,i)