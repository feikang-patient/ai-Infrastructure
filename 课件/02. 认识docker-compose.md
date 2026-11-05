# 认识 Docker Compose

## 动机

在真实的企业开发中，无论是传统的后端应用，还是 Agent 应用，都需要一系列基础设施作为支持。

比如，一个 Agent 应用需要：

- `langfuse`：实现 Agent 的观察与评估
- `PostgreSQL`：存储业务数据，比如：用户会话、检查点、DataSet 等等
- `Redis`：存储临时数据，比如缓存、消息队列等
- `minio`：对象存储，保存静态数据
- `clickhouse`：存储日志、指标等分析型数据，可进行高速统计查询
- `pgadmin`：数据管理控制面
- ...

这些基础设施在开发阶段，往往都是以 Docker容器 的形态启动。

如果分开管理，就涉及到一系列的问题：

1. 容器之间如何通信

   只能手动的把它们加到一个docker网络。

2. 每个容器需要的环境变量不一致

   只能在每次启动容器时，手动给它设置环境变量。

3. 容器间存在依赖怎么处理？

   只能在脑海中记住它们的依赖关系：先启动被依赖的容器，再启动依赖它的容器。

我们希望以上问题能以更加简洁、优雅、自动化的方式处理。

这就要依靠`Docker Compose`。

`Docker Compose`称之为容器编排，它允许通过一个配置文件（`docker-compose.yml`），集中性的管理一个企业级工程所需要的所有容器。

简单来说：`Docker Compose`提供一个入口，通过该入口，统一管理多个容器。

## 认识 docker-compose.yml

```yaml
name: deal-pilot  # 提供一个分组名称，所有的容器都收归进该分组，通常为项目名称

services: # 核心配置，描述当前分组下，有哪些服务，每个服务对应一个容器
	pgadmin: 
	langfuse-worker:
	langfuse-web:
	clickhouse:
	minio:
	redis:
	postgres:
	
volumes:	# 卷柜声明，每个卷柜就是一个磁盘存储空间
	postgres_data:
	clickhouse_data:
	clickhouse:logs:
```

## 常用命令

```shell
# 创建并在后台启动所有容器
docker compose up -d

# 查看容器状态
docker compose ps

# 持续查看所有容器的日志，按 Ctrl+C 退出
docker compose logs -f

# 停止容器，但保留容器
docker compose stop

# 启动已经停止的容器
docker compose start

# 重启所有容器
docker compose restart

# 停止并删除容器和网络，不会删除数据卷
docker compose down

# 重新创建并在后台启动所有容器
docker compose up -d --force-recreate
```

