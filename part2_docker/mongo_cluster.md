## mongo集群分片

概念文章1：https://developer.ibm.com/zh/articles/os-mongodb-sharded-cluster/

操作文章2：https://blog.csdn.net/yekoufeng/article/details/83412431#mongosmongos_103

操作视频：https://www.bilibili.com/video/BV1p4411J7sq?from=search&seid=3909948528816913046

配置文件1: https://www.jb51.net/article/161315.htm

https://www.cnblogs.com/phpandmysql/p/7763394.html

### 搭建集群(docker伪集群)

| 集群角色      | docker名称 | docker内部端口 | 挂载路径                         | 介绍                 |
| ------------- | ---------- | -------------- | -------------------------------- | -------------------- |
| Config Server | configsvr0 | 10.1.1.2:27019 | /home/mongodb/data/cs/configsvr0 | 服务复制集           |
| Config Server | configsvr1 | 10.1.1.3:27019 | /home/mongodb/data/cs/configsvr1 | 服务复制集           |
| Shard Server  | shardsvr00 | 10.1.1.4:27018 | /home/mongodb/data/sh/shardsvr00 | 分片复制集(数据存储) |
| Shard Server  | shardsvr01 | 10.1.1.5:27018 | /home/mongodb/data/sh/shardsvr01 | 分片复制集           |
| Shard Server  | shardsvr10 | 10.1.1.6:27018 | /home/mongodb/data/sh/shardsvr10 | 分片复制集           |
| Shard Server  | shardsvr11 | 10.1.1.7:27018 | /home/mongodb/data/sh/shardsvr11 | 分片复制集           |
| Mongos        | mongos0    | 10.1.1.8:27017 | 无                               | 连接(路由)           |
| Mongos        | mongos1    | 10.1.1.9:27017 | 无                               | 备用连接             |

**1、拉取mongo镜像**

```shell
# 拉取mongo镜像
docker pull docker
# 为MongoDB集群创建独立的docker网桥
docker network create --subnet=10.1.1.0/24 mongodb0
```

**2、创建配置复制集**

运行三个配置复制集

```shell
# 配置复制集1
docker run -d --name configsvr0 --network=mongodb0 --ip=10.1.1.2 --restart=always -v /home/mongodb/data/cs/configsvr0:/data/configdb mongo --configsvr --replSet "rs_configsvr" --bind_ip_all --wiredTigerCacheSizeGB 4
# 配置复制集2
docker run -d --name configsvr1 --network=mongodb0 --ip=10.1.1.3 --restart=always -v /home/mongodb/data/cs/configsvr1:/data/configdb mongo --configsvr --replSet "rs_configsvr" --bind_ip_all --wiredTigerCacheSizeGB 4
# 配置复制集3
docker run -d --name configsvr2 --network=mongodb0 --ip=10.1.1.4 --restart=always -v /home/mongodb/data/cs/configsvr2:/data/configdb mongo --configsvr --replSet "rs_configsvr" --bind_ip_all --wiredTigerCacheSizeGB 4

# 另外，可以指定配置文件 默认无配置文件
docker run --name some-mongo -v /my/custom:/etc/mongo -d mongo --config /etc/mongo/mongod.conf
```



查询复制集的ip地址

```
docker inspect configsvr0 | grep IPAddress
docker inspect configsvr1 | grep IPAddress
docker inspect configsvr2 | grep IPAddress
```

由于–configsvr的默认端口为27019，所以我的配置服务的地址为 

- configsvr0: 10.1.1.2:27019
- configsvr1: 10.1.1.3:27019
- configsvr2: 10.1.1.4:27019

初始化配置复制集

```shell
# 进入容器
docker exec -it configsvr0 bash
# 进入mongo
mongo --host 10.1.1.2 --port 27019
# mongo中运行
rs.initiate({
	_id: "rs_configsvr",
	configsvr: true,
	members: [
	{ _id : 0, host : "10.1.1.2:27019" },
    { _id : 1, host : "10.1.1.3:27019" },
	{ _id : 2, host : "10.1.1.4:27019" }
	]
})
```

**3、创建分片复制集**

```shell
# 第一个分片复制集
docker run --name shardsvr00 --network=mongodb0 --ip=10.1.1.5 --restart=always -d -v /home/mongodb/data/sh/shardsvr00:/data/db mongo --shardsvr --replSet "rs_shardsvr0" --bind_ip_all
docker run --name shardsvr01 --network=mongodb0 --ip=10.1.1.6 --restart=always -d -v /home/mongodb/data/sh/shardsvr01:/data/db mongo --shardsvr --replSet "rs_shardsvr0" --bind_ip_all
docker run --name shardsvr02 --network=mongodb0 --ip=10.1.1.7 --restart=always -d -v /home/mongodb/data/sh/shardsvr02:/data/db mongo --shardsvr --replSet "rs_shardsvr0" --bind_ip_all
# 第二个分片复制集
docker run --name shardsvr10 --network=mongodb0 --ip=10.1.1.8 --restart=always -d -v /home/mongodb/data/sh/shardsvr10:/data/db mongo --shardsvr --replSet "rs_shardsvr1" --bind_ip_all
docker run --name shardsvr11 --network=mongodb0 --ip=10.1.1.9 --restart=always -d -v /home/mongodb/data/sh/shardsvr11:/data/db mongo --shardsvr --replSet "rs_shardsvr1" --bind_ip_all
docker run --name shardsvr12 --network=mongodb0 --ip=10.1.1.10 --restart=always -d -v /home/mongodb/data/sh/shardsvr12:/data/db mongo --shardsvr --replSet "rs_shardsvr1" --bind_ip_all
# 第三个分片复制集
docker run --name shardsvr20 --network=mongodb0 --ip=10.1.1.11 --restart=always -d -v /home/mongodb/data/sh/shardsvr20:/data/db mongo --shardsvr --replSet "rs_shardsvr2" --bind_ip_all
docker run --name shardsvr21 --network=mongodb0 --ip=10.1.1.12 --restart=always -d -v /home/mongodb/data/sh/shardsvr21:/data/db mongo --shardsvr --replSet "rs_shardsvr2" --bind_ip_all
docker run --name shardsvr22 --network=mongodb0 --ip=10.1.1.13 --restart=always -d -v /home/mongodb/data/sh/shardsvr22:/data/db mongo --shardsvr --replSet "rs_shardsvr2" --bind_ip_all
```

查询复制集的ip地址

```
docker inspect shardsvr00 | grep IPAddress
docker inspect shardsvr01 | grep IPAddress
docker inspect shardsvr02 | grep IPAddress
docker inspect shardsvr10 | grep IPAddress
docker inspect shardsvr11 | grep IPAddress
docker inspect shardsvr12 | grep IPAddress
docker inspect shardsvr20 | grep IPAddress
docker inspect shardsvr21 | grep IPAddress
docker inspect shardsvr22 | grep IPAddress
```

由于–configsvr的默认端口为27018，所以我的配置服务的地址为 

- shardsvr00: 10.1.1.5:27018
- shardsvr01: 10.1.1.6:27018
- shardsvr02: 10.1.1.7:27018
- shardsvr10: 10.1.1.8:27018
- shardsvr11: 10.1.1.9:27018
- shardsvr12: 10.1.1.10:27018
- shardsvr20: 10.1.1.11:27018
- shardsvr21: 10.1.1.12:27018
- shardsvr22: 10.1.1.13:27018

初始化配置复制集

```shell
# 进入容器
docker exec -it shardsvr00 bash
# 进入mongo
mongo --host 10.1.1.5 --port 27018
# mongo中运行
rs.initiate({
	_id : "rs_shardsvr0",
	members: [
		{ _id : 0, host : "10.1.1.5:27018" },
		{ _id : 1, host : "10.1.1.6:27018" },
		{ _id : 2, host : "10.1.1.7:27018" }
	]
})
```

```shell
# 进入mongo
mongo --host 10.1.1.8 --port 27018
# mongo中运行
rs.initiate({
	_id : "rs_shardsvr1",
	members: [
	{ _id : 0, host : "10.1.1.8:27018" },
	{ _id : 1, host : "10.1.1.9:27018" },
	{ _id : 2, host : "10.1.1.10:27018" }
	]
})

# 进入mongo
mongo --host 10.1.1.11 --port 27018
# mongo中运行
rs.initiate({
	_id : "rs_shardsvr2",
	members: [
	{ _id : 0, host : "10.1.1.11:27018" },
	{ _id : 1, host : "10.1.1.12:27018" },
	{ _id : 2, host : "10.1.1.13:27018" }
	]
})
```

**4、创建mongos，连接mongos到分片集群**

由于镜像的默认入口是 mongod，所以要通过 --entrypoint “mongos” 将其改为 mongos：

```shell
docker run --name mongos0 --network=mongodb0 --ip=10.1.1.14 --restart=always -d -p 27017:27017 --entrypoint "mongos" mongo --configdb rs_configsvr/10.1.1.2:27019,10.1.1.3:27019,10.1.1.4:27019 --bind_ip_all
# 第二个
docker run --name mongos1 --network=mongodb0 --ip=10.1.1.15 --restart=always -d -p 27018:27017 --entrypoint "mongos"  mongo --configdb rs_configsvr/10.1.1.2:27019,10.1.1.3:27019,10.1.1.4:27019 --bind_ip_all

```

查看地址

```
docker inspect mongos0 | grep IPAddress
docker inspect mongos1 | grep IPAddress

```

默认端口为27017，故地址为：

- 10.1.1.14：27017
- 10.1.1.14：27017

注：映射到宿主机便于外面客户端访问

**5、添加分片到集群**

```shell
docker exec -it mongos0 bash
mongo --host 10.1.1.14 --port 27017
# mongo中运行
sh.addShard("rs_shardsvr0/10.1.1.5:27018,10.1.1.6:27018,10.1.1.7:27018")
sh.addShard("rs_shardsvr1/10.1.1.8:27018,10.1.1.9:27018,10.1.1.10:27018")
sh.addShard("rs_shardsvr2/10.1.1.11:27018,10.1.1.12:27018,10.1.1.13:27018")

```

其它操作

```shell
# mongos中
# 查看分片 
db.runCommand({listshards:1})
# 查看分片状态
sh.status()

```

**6、数据库启用分片**

```shell
# 上一步不退出docker 继续运行
sh.enableSharding("industry")
sh.enableSharding("national_conditions")

```

**7、集合的分片操作**

**7.1 基于Ranged的分片操作**

基于范围分片特别适合范围查找，因为可以直接定位到分片，所以效率很高。

**分片的键必须是索引(也可以为联合索引)**

以下为具体操作步骤：

1. 开启 test 库的分片功能。

   ```
   sh.enableSharding("test")
   
   ```

2. 选择集合的分片键，此时 MongoDB 会自动为 age 字段创建索引。

   ```
   sh.shardCollection("test.test_shard",{"age": 1})
   sh.shardCollection("industry.C25_data",{"_id":1})
   
   ```

3. 批量造测试数据。

   ```
   use test
   for (i = 1; i < = 20000; i++) db.test_shard.insert({age:(i%100), name:"user"+i,
   create_at:new Date()})
   
   ```

4. 观察分片效果。以下为命令和部分输出示例：

   ```
   sh.status()
   test.test_shard
   shard key: { "age" : 1 }
   unique: false
   balancing: true
   chunks:
           rep_shard1    2
           rep_shard2    3
   { "age" : { "$minKey" : 1 } } --<< { "age" : 0 } on : rep_shard1 Timestamp(2, 0)
   { "age" : 0 } --<< { "age" : 36 } on : rep_shard1 Timestamp(3, 0)
   { "age" : 36 } --<< { "age" : 73 } on : rep_shard2 Timestamp(2, 3)
   { "age" : 73 } --<< { "age" : 92 } on : rep_shard2 Timestamp(2, 4)
   { "age" : 92 } --<< { "age" : { "$maxKey" : 1 } } on : rep_shard2 Timestamp(3, 1)
   
   ```

   从输出结果可以看到 `test.test_shard` 集合总共有 2 个分片，分片 rep_shard1 上有 2 个 chunk，分片 rep_shard2 上有 3 个 chunk，年龄大于或等于 0 并且小于 36 的文档数据放到了第一个分片 rep_shard1，年龄大于或等于 36 并且小于 73 的文档数据放到了第二个分片 rep_shard2，此时已经达到了分片的效果。我们可以使用 `find` 命令来确认是否对应的数据存在相应的分片，以下为命令和部分输出示例：

   ```
   db.test_shard.find({ age: { $gte : 36 ,$lt : 73 } }).explain()
   {
    "queryPlanner" : {
        "winningPlan" : {
            "stage" : "SINGLE_SHARD",
            "shards" : [
                {
                    "shardName" : "rep_shard2",
                    "connectionString" : "rep_shard2/10.0.4.6:27019,10.0.4.7:27019,10.0.4.8:27019",
                    "namespace" : "test.test_shard",
                    "winningPlan" : {
                        "stage" : "FETCH",
                        "inputStage" : {
                            "stage" : "SHARDING_FILTER",
                            "inputStage" : {
                                "stage" : "IXSCAN",
                                "keyPattern" : {
                                    "age" : 1
                                },
                                "indexName" : "age_1",
                                "direction" : "forward",
                                "indexBounds" : {
                                    "age" : [
                                        "[36.0, 73.0)"
                                    ]
                                }
                            }
                        }
                    },
                }
            ]
        }
    }
   }
   
   ```

	从以上输出结果可以看到，当查找年龄范围为大于等于 36 并且小于 73 的文档数据，MongoDB 会直接定位到分片 rep_shard2，从而避免全分片扫描以提高查找效率。如果将 `$gte : 36` 改为 `$gte : 35` ，结果会是怎么样的呢？答案是 MongoDB 会扫描全部分片，执行计划的结果将由 `SINGLE_SHARD` 变为 `SHARD_MERGE` ，如果感兴趣，您可以自行验证。

**7.2 基于Hashed的分片操作**

1. 开启 test 库的分片功能。

   ```
   sh.enableSharding("test")
   
   ```

   显示更多

2. 选择集合的分片键，注意这里创建的是 hash 索引。

   ```
   sh.shardCollection("test.test_shard",{"age": "hashed"})
   
   ```

   显示更多

3. 批量造测试数据。

   ```
   use test
   for (i = 1; i <= 20000; i++) db.test_shard.insert({age:(i%100), name:"user"+i, create_at:new Date()})
   
   ```

   显示更多

4. 观察分片效果。以下为命令和部分输出示例：

   ```
   sh.status()
   chunks:
           rep_shard1    2
           rep_shard2    2
   { "age" : { "$minKey" : 1 } } --<< { "age" : NumberLong("-4611686018427387902") } on : rep_shard1 Timestamp(1, 0)
   { "age" : NumberLong("-4611686018427387902") } --<< { "age" : NumberLong(0) } on : rep_shard1 Timestamp(1, 1)
   { "age" : NumberLong(0) } --<< { "age" : NumberLong("4611686018427387902") } on : rep_shard2 Timestamp(1, 2)
   { "age" : NumberLong("4611686018427387902") } --<< { "age" : { "$maxKey" : 1 } } on : rep_shard2 Timestamp(1, 3)
   
   ```

   通过以上输出可以看到，对于等值查找，基于 Hashed 分片查找效率很高，直接定位到一个分片就可以返回满足条件的数据，无需进行全部分片的查找。

### 其它命令

```shell
删除命令
db.runCommand({removeShard:"rs_shardsvr1"})

```

balaece

### 配置修改

详情请看mongo中文社区

```shell
# 找到主节点
cfg = rs.conf();
cfg.members[0].host = "10.1.1.5:27019"
cfg.members[1].host = "10.1.1.6:27019"
cfg.members[2].host = "10.1.1.7:27019"
rs.reconfig(cfg)

```