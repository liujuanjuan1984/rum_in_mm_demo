# rum_in_mm_demo

1、安装

```sh 
pipenv install
```

mixin-python-sdk 及 rum light-node-sdk（npm）需手动安装


2、部署：


2.1 在 https://developers.mixin.one/ 申请 app，生成应用 session，保存到 根目录下的 mixin_bot_keystore.json

2.2 从 rum 全节点处获取 seed 和 host、jwt token 等。

可自行编译 rum fullnode binary 并运行 start_rum_fullnode.bat （需要已支持 eth key 的版本），然后调用 src/tool.py 来创建 group

注意配置 src/config_rss.py 中的参数。

2.3 运行 blaze 和 rss 服务，其中 blaze 负责监听消息，rss 负责把消息发送到 rum group 上。


```sh
pipenv run python src/bot_blaze.py
pipenv run python src/bot_rss.py

```


### others

reform: 

```sh
isort .
black -l 80 -t py37 -t py38 -t py39 -t py310 .
black -l 120 -t py37 -t py38 -t py39 -t py310 .
```


```bat
::rum rum fullnode
D:
cd D:\RUM-DATA-ETH
set RUM_KSPASSWD=your-pwd
.\quorum_full_eth.exe -peername peer -listen /ip4/0.0.0.0/tcp/31123 -listen /ip4/0.0.0.0/tcp/31124/ws  -apihost 127.0.0.1 -apiport 31194 -peer /ip4/94.23.17.189/tcp/10666/p2p/16Uiu2HAmGTcDnhj3KVQUwVx8SGLyKBXQwfAxNayJdEwfsnUYKK4u -configdir rum_test/peerConfig -datadir rum_test/peerData -keystoredir rum_test/keystore -debug=true
```
