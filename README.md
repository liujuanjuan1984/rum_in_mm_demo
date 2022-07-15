# rum_in_mm_demo

#### 这是什么？

以 mixin bot 为入口/交互场景，mixin 用户可直接对该 bot 发送消息；bot 将为每个用户映射一个 rum account，并把消息采用 rum account 签名并加密后，发送到 rum group 上。

#### 它如何工作？

[图示](https://www.figma.com/community/file/1129621232505390719 )

#### 实例

mixin bot: 7000103264

## 部署与运行

依照下述步骤，你也可以创建并部署相似的服务。

### 1、安装

#### Python 依赖：

```sh
pipenv install
```

主要用到 eth_account 处理账号, rumpy 处理与 quorum 交互，和 mixin-python-sdk 处理消息监听，其中 [mixin-sdk-python](https://github.com/liujuanjuan1984/mixin-sdk-python) 需手动安装（它的 main 版本尚未稳定，我 fork 的这个版本能跑通。）

#### JavaScript 依赖：

主要用到 rum-light-node-sdk（npm），调用它的方法，提供私钥和数据，得到加密后的数据。

```sh
cd src/js
npm install quorum-light-node-sdk

```

### 2、部署

#### 依赖：mixin bot

前往 https://developers.mixin.one/ 申请 app，生成应用 session，保存到 根目录下的 mixin_bot_keystore.json

#### 依赖：rum group & fullnode

采用 rum fullnode 创建 group，并获取 group seed 和 apihost:port、jwt token 等接口信息。

可自行编译 rum fullnode binary 并运行（需要已支持 eth account 的版本，该版本还很新，尚未发布到 main），然后调用 src/tool.py 来创建 group。也可以由其它 fullnode 提供接口。fullnode 不需要与其它服务运行在同一台设备上。

```bat
::rum rum fullnode
D:
cd D:\RUM-DATA-ETH
set RUM_KSPASSWD=your-pwd
.\quorum_full_eth.exe -peername peer -listen /ip4/0.0.0.0/tcp/31123 -listen /ip4/0.0.0.0/tcp/31124/ws  -apihost 127.0.0.1 -apiport 31194 -peer /ip4/94.23.17.189/tcp/10666/p2p/16Uiu2HAmGTcDnhj3KVQUwVx8SGLyKBXQwfAxNayJdEwfsnUYKK4u -configdir rum_test/peerConfig -datadir rum_test/peerData -keystoredir rum_test/keystore -debug=true
```

注意修改 src/config_rss.py 中的相关参数。

#### 监听和转发

运行本仓库提供的 blaze 和 rss 服务，其中 blaze 负责监听消息，rss 负责把消息发送到 rum group 上。


```sh
pipenv run python src/bot_blaze.py
pipenv run python src/bot_rss.py

```

## 其它

Python 代码格式化：

```sh
isort .
black -l 80 -t py37 -t py38 -t py39 -t py310 .
black -l 120 -t py37 -t py38 -t py39 -t py310 .
```

非常早期的 demo，欢迎交流！