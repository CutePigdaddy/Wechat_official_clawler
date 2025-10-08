## 🗄️ 主要功能说明
抓取微信公众号文章
可以通过URL短链获取微信公众号文章html源码和内容/可以通过手动获取headers和URL来抓取公众号前十文章列表
## 🗄️ 使用说明
先创建venv虚拟环境 `python -m venv venv`
然后激活虚拟环境 `.venv\Scripts\Activate.ps1`
下载必要第三方库`pip install -r requirements.txt`
启动 `python main.py`
根据指引来就行，需要自学Fiddler抓取headers和URL
## 🗄️ DB说明

主要函数都在 `db_operations.py` 里面。

在根目录的你的 `.py` 文件里面：
```python
from db.db_operations import *
```
db_operations.py里面有函数介绍
