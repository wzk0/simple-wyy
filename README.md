# simple-wyy
一个功能和界面都简单的网易云前后端

## 效果

demo! >> https://simple-wyy-production.up.railway.app

![首页](https://ghproxy.com/https://raw.githubusercontent.com/wzk0/photo/main/202210192122486.png)

![搜索](https://ghproxy.com/https://raw.githubusercontent.com/wzk0/photo/main/202210192122895.png)

![搜索结果](https://ghproxy.com/https://raw.githubusercontent.com/wzk0/photo/main/202210192123863.png)

![热搜](https://ghproxy.com/https://raw.githubusercontent.com/wzk0/photo/main/202210192123841.png)

![单页](https://ghproxy.com/https://raw.githubusercontent.com/wzk0/photo/main/202210200952765.png)

## 部署

### 服务器端

可以直接`fork`此仓库,更改细节后在`railway`中免费部署.

> 细节可以是`cookies(如果你是vip的话就能有vip啦!)`,`api(nodejs版本的api!)`

已经写好了`Dockerfile`,无需自己啊巴啊巴.

### 本地

在确保电脑上有git的情况下执行如下指令:

```
git clone https://github.com/wzk0/simple-wyy && cd simple-wyy
pip install -r requirements.txt
export FLASK_APP=start
flask run
```

## 开发

使用到了网易云API - https://github.com/Binaryify/NeteaseCloudMusicApi

单页在线播放器为APlayer - https://aplayer.js.org/#/zh-Hans/