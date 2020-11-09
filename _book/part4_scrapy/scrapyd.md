# scrapyd部署(window端)

## 介绍

需要安装以下库 `pip install [库名]`

scrapyd：服务器端

scrapyd-client：客户端

scrapyd-deploy：一个工具，打包egg并且自动化部署到服务器



## 部署步骤

参考于简书（https://www.jianshu.com/p/ddd28f8b47fb）

1. 打开服务端端：命令行运行scrapyd,配置成功会生成dbs和eggs文件夹
2. 在项目文件夹下，修改scrapy.cfg配置文件，取消url的注释
3. 在项目文件夹下，测试scrapyd-deploy（windows），参考以上网址修改
4. 将项目部署到服务器`scrapyd-deploy [deploy名] -p [项目名]`
5. 启动项目：`curl http://localhost:6800/schedule.json -d project=[项目名] -d spider=[spider名]`



- scrapy.cfg的修改

> [deploy:demo]
> url = http://192.168.0.11:6800/addversion.json

- 部署运行


```shell
scrapyd-deploy demo -p [项目名]  # 部署到服务器

# 运行spider
curl http://192.168.0.11:6800/schedule.json -d project=[] -d spider=[]

```
| 操作                                                         | 解释                     |
| ------------------------------------------------------------ | ------------------------ |
| `scrapyd-deploy [deploy名] -p [项目名]`                      | 将项目部署到服务器       |
| `curl http://localhost:6800/schedule.json -d project=[项目名] -d spider=[spider名]` | 启动项目                 |
| `curl http://localhost:6800/daemonstatus.json`               | 查看服务端状态           |
| `curl http://192.168.0.11:6800/listprojects.json`            | 列出上传的项目列表       |
| `curl http://192.168.1.9:6800/listversions.json\?project\=[项目名]` | 列出有某个上传项目的版本 |
| `curl http://192.168.1.9:6800/cancel.json -d project=[项目名]-d job=[job id]` |  取消爬虫运行                        |


