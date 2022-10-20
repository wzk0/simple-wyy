# simple-wyy
一个功能和界面都简单的网易云前后端

## 效果

demo! >> https://simple-wyy-production.up.railway.app

## 部署

### 服务器端

可以直接`fork`此仓库,更改细节后在`railway`中免费部署.

> 细节可以是`start.py`中的`cookies(如果你是vip的话就能有vip啦!)`,`api(nodejs版本的api!)`

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

前端表面上简洁,实际暗流涌动...请前端大佬不要F12!