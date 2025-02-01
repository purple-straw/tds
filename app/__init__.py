"""
@Project ：tds_dev 
@File    ：__init__.py.py
@IDE     ：PyCharm 
@Author  ：靓仔
@Date    ：2025/1/21 0021 20:35 
"""

from flask import Flask
from app.web.routes import api


def create_app():
    app = Flask(__name__,
                static_folder='web/static',
                template_folder='web/templates')

    # 注册蓝图
    app.register_blueprint(api, url_prefix='/api')

    # 添加CORS支持
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    return app


# 创建应用实例
app = create_app()
