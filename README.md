TDS (Talent Data Sync) 人才数据同步系统
项目简介
TDS 是一个专门用于组织人才数据同步和对比的系统，它能够实时比对 API 和数据库中的人才数据，帮助管理者快速发现和处理数据不一致的问题。系统采用 DDD（领域驱动设计）架构，提供了直观的 Web 界面来展示数据对比结果。

主要功能
数据对比分析

总人数对比
职级分布对比
平均年龄对比
人员详细信息对比
数据可视化

职级分布图表
匹配率统计
数据差异展示
数据管理

人员信息查看
数据编辑
数据同步状态监控
技术栈
后端
Python 3.8+
Flask Web 框架
SQLAlchemy ORM
MySQL 数据库
前端
HTML5/CSS3
JavaScript (ES6+)
Bootstrap 5
Chart.js 图表库
工具和库
requests：HTTP 请求
python-dotenv：环境变量管理
urllib3：HTTP 客户端
PyMySQL：MySQL 驱动
Flask-CORS：跨域资源共享
系统架构
项目采用 DDD（领域驱动设计）架构，分为以下几层：

表现层 (Presentation Layer)

Web 界面
API 接口
数据展示
应用层 (Application Layer)

应用服务
数据协调
业务流程编排
领域层 (Domain Layer)

领域实体
领域服务
值对象
基础设施层 (Infrastructure Layer)

数据持久化
外部服务集成
工具类
项目结构
app/
├── application/          # 应用服务层
├── domain/              # 领域层
│   └── organization/    # 组织领域
├── infrastructure/      # 基础设施层
├── web/                 # Web 界面
│   ├── static/         # 静态资源
│   └── templates/      # 模板文件
├── config/             # 配置文件
├── utils/              # 工具类
└── services/           # 服务实现
快速开始
环境准备

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
配置环境变量

# 创建 .env 文件并配置以下变量
FLASK_APP=run_web.py
FLASK_ENV=development
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DB=tds
初始化数据库

# 确保 MySQL 服务已启动
# 创建数据库和表结构
python init_db.py
启动应用

# 运行 Flask 应用
flask run
访问系统

在浏览器中访问: http://localhost:5000
开发规范
代码风格

遵循 PEP 8 规范
使用类型注解
编写详细的文档字符串
提交规范

feat: 新功能
fix: 修复问题
docs: 文档修改
style: 代码格式修改
refactor: 代码重构
test: 测试用例修改
chore: 其他修改
注意事项
确保 .env 文件中包含所有必要的环境变量
数据库连接信息需要正确配置
API 接口需要有效的访问凭证
建议在虚拟环境中运行项目
定期备份数据库
贡献指南
Fork 项目
创建特性分支
提交更改
推送到分支
创建 Pull Request
许可证
MIT License
