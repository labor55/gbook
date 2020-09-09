# git

## 一、git 描述&安装初始化

git是版本管理工具，一般可用于gitlab、github、码云（gitee）等代码管理网站

git 分为三个区：工作区，暂存区和版本库

- 工作区

  一般指本地磁盘，拥有.git（隐藏文件夹）的文件夹

- 暂存区

  在版本库和工作区之间，相当于文件中转站

- 版本库

  ​	就是仓库,分为本地仓库和远程仓库（gitlab等）



git下载：https://github.com/waylau/git-for-win/

安装一直next就行

刚下载完git 配置下用户名

打开git命令行输入以下命令

> git config --global user.name "your name"
>
> git config --global user.email  "your email"

查看用户信息

> git config -l

可以看见用户刚配置的用户和系统信息



## 二、Git指令

### 生成本地ssh

1. 进入Administrator的`.ssh`文件夹下，运行git-bash, 命令

   `ssh-keygen -t rsa -C "your email"`

2. 输入该ssh的名字

3. 输入密码（可不写）

4. 将.pub文件内容粘贴到你的gitlab上

5. 这样你就可以使用ssh的url进行上传文件了

### 基本指令

| 指令                                       | 解释                                   |
| ------------------------------------------ | -------------------------------------- |
| git config --global user.name "your name"  | 初始化用户名                           |
| git config --global user.email"your email" | 初始化邮箱                             |
| git init                                   | 创建一个本地git仓库                    |
| git add .                                  | 添加修改的提交到暂存区                 |
| git commit -m"commit message"              | 提交并注释                             |
| git remote add [name] [url.git]            | 添加远程仓库地址                       |
| git push                                   | 本地推送至远程                         |
| git pull/fetch                             | 远程下载到本地                         |
| git clone [url.git]                        | 下载到本地                             |
| git log                                    | 查看提交日志                           |
| git status                                 | 查看仓库状态                           |
| git remote add [远程名] [git地址]          | 将本地关联到远程                       |
| git remote  [-v]                           | 查看本地关联的远程名，可以关联多个远程 |
| git remote rm [远程名]                     | 删除关联的远程                         |

http://192.168.0.11/b_07/scrapy_zhengce_v1_07.git

git@192.168.0.11:b_07/scrapy_zhengce_v1_07.git

### 回滚撤销

[请戳此处](https://blog.csdn.net/ligang2585116/article/details/71094887)



### 分支指令

创建分支

> git branch [b-name]

切换分支

> git checkout [b-name]

分支合并

> git merge

列出分支

> git branch

删除分支

> git branch -d [b-name]



[请戳此处](https://www.runoob.com/git/git-branch.html)



## 三、工作提交

两种方法，建议使用第一种方法

### 1、

1. 创建一个gitlab的仓库项目，复制http的git地址

2. `git clone [url.git]`  下载到本地

3. 进入到刚下载的git 文件夹， 把你要上传的文件，复制到此文件夹，修改README.md文件

4. `git add .` ---->   `git commit -m"your commit message"`----> `git push`

### 2、

1. 建立一个远程仓库

2. 创建一个空文件夹，使用`git init` 变成本地git库

3. 添加远程仓库地址

   > git remote add [origin] [git地址]

4. 先使用`git pull origin master master`,将远程推送至本地
5. 将你要上传的文件放入此git文件夹
6. `git push origin master`上传到远程仓库

以后还有补充，大家先用着这么多