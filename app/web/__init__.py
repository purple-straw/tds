from flask import Flask
from .routes import api

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(api, url_prefix='/api')

# 其他初始化代码... 