### python环境
- py3.7
- pip install tronado
- pip install peewee

### web环境
- nodejs
- yarn

### 数据库
- 放置于项目根目录下命名为dataset.db

### 本地构建项目
- web目录下 命令行 
  - yarn install   
  - yarn build
### 运行
- 启动/server/server.py

### 配置ip端口等
- web/src/config/config.json

示例:
```
  "ip":"localhost", 服务器ip
  "port":8888,    服务器端口
  "db_path":"../dataset.db"  db文件相对于 server/server.py的相对路径 默认路径为项目根目录
```  

# 注意  
- 修改配置文件后需要重新执行yarn build 并重启server 才能让网页配置生效