## 1、scrapyd镜像

**系统介绍**

基础镜像:python:3.7-buster

系统: ubuntu系统

python环境: py3.7.8

pip版本: pip3 版本为 20.2.2

系统apt源: 阿里源

pip源: 豆瓣源:https://pypi.douban.com/simple/

**容器中**

pip-->pip3 pip3-->pip3
python-->python3.7 python3-->python3.7

安装pip库: requirement.txt + pycommon0.0.6 + logparser

安装编辑软件: vim

环境变量: PYTHONIOENCODING=utf-8, TZ=Asia/Shanghai

映射端口: 6800



### 1、准备镜像

**1.1 基础镜像**

```shell
# 拉取镜像
sudo docker pull python:3.7-buster
# 生成镜像
sudo docker build -t py37/scrapyd .
```

**1.2 编写Dockerfile文件**

```dockerfile
FROM python:3.7-buster
# 换源,并更新源
RUN rm /etc/apt/sources.list
COPY sources.list /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 40976EAF437D05B5
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y vim

# 设置工作目录
RUN mkdir /app
# 选择工作文件夹
WORKDIR /app
# 设置环境变量
ENV PYTHONIOENCODING=utf-8
ENV TZ=Asia/Shanghai

# 安装包
COPY requirement.txt /app
RUN pip install -r requirement.txt -i https://pypi.douban.com/simple/

EXPOSE 6800
CMD ["scrapyd"]
```

**1.3 sources.list文件**

使用阿里源

```
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
```

**1.4 预安装py库**

requirement.txt

```
scrapyd==1.2.1
scrapyd-client==1.1.0
requests==2.22.0
pymongo==3.9.0
PyMySQL==0.9.3
Scrapy==1.8.0
fake-useragent==0.1.11
lxml==4.4.2
selenium==3.141.0
retrying==1.3.3
PyExecJS==1.5.1
bs4==0.0.1
uuid==1.30
peewee==3.13.3
retrying==1.3.3
```

**1.5 运行指令**

(要求:docker命名和挂载目录名称都是 --> scrapyd_你的名字_你的端口, 例如scrapyd_lab_6822,可以在一下命令后面指定运行指令:/app/start.sh,默认为scrapyd)

```
sudo docker run -it -d --name [scrapyd_xxx_68xx] --restart=always -p 68xx:6800 -v /scrapyd_apps/scrapyd_xxx_6800:/app py37/scrapyd
```

## 2、scrapydweb镜像

基础镜像：python:3.7-buster

**Dockerfile文件**

```
FROM python:3.7-buster
# 换源
RUN rm /etc/apt/sources.list
COPY sources.list /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 40976EAF437D05B5
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y vim

# 设置工作目录
RUN mkdir /app
WORKDIR /app

# 设置环境变量
ENV PYTHONIOENCODING=utf-8
ENV TZ=Asia/Shanghai

# 安装包
RUN pip install scrapydweb -i https://pypi.douban.com/simple/
EXPOSE 5000
CMD ["scrapydweb"]
```

**运行指令**

```
# 生成镜像
sudo docker build -t py37/scrapydweb .
# 生成容器
sudo docker run -it -d --name scrapydweb_5000 --restart=always -p 5000:5000 -v /scrapyd_apps/scrapydweb:/app py37/scrapydweb
```

