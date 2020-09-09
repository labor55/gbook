## mysql

```shell
docker run -p 3306:3306 --name mysql \
-v /home/mysql/conf:/etc/mysql \
-v /home/mysql/logs:/var/log/mysql \
-v /home/mysql/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=jskj61776099 \
-d mysql:5.7
```

## redis

1. 从官网获取 [redis.conf](http://download.redis.io/redis-stable/redis.conf) 配置文件 	
   - 修改默认配置文件 		
     - bind 127.0.0.1 #注释掉这部分，这是限制redis只能本地访问
     - protected-mode no #默认yes，开启保护模式，限制为本地访问
     - daemonize no#默认no，改为yes意为以守护进程方式启动，可后台运行，除非kill进程（可选），改为yes会使配置文件方式启动redis失败
     - dir  ./ #输入本地redis数据库存放文件夹（可选）
     - appendonly yes #redis持久化（可选）
2.  docker 启动 redis 命令

```shell
docker run -p 6379:6379 --restart=always --name redis --privileged=true -v /home/redis/redis.conf:/etc/redis/redis.conf -v /home/redis/data:/data -d redis redis-server /etc/redis/redis.conf
```

## proxy_pool

```
docker run --env DB_CONN=redis://192.168.3.85:6379/0 -p 5010:5010 -v /home/proxypool:/app --net=host --name proxypool -d jhao104/proxy_pool:latest
```

## gitbook

```
docker create -v /home/book:/srv/gitbook -p 4000:4000 --name gbook fellah/gitbook
```

