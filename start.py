from flask import Flask,render_template,request,redirect,url_for
import requests
import json

app = Flask(__name__,template_folder='./static/templates')
api='https://wyyapi-wzk0.vercel.app' ##网易云api地址
cookies={
'MUSIC_U':'',
'NMTID':'',
'__csrf':'',
'__remember_me': 'true'
} ##cookies

##解析列表得到歌手
def get_ar(ls):
    ar=[]
    for a in ls:
        ar.append(a['name'])
    return ','.join(ar)

##解析得到歌曲信息
def analyze(dic):
    ls=[]
    for l in dic['result']['songs']:
        ar=[]
        for ll in l['ar']:
            ar.append(ll['name'])
        d={'title':l['name']+' - '+','.join(ar),'year':str(l['id']),'link':'/dl/%s'%str(l['id']),'word':'跳转至单曲页面⚡️'}
        ls.append(d)
    return ls

##解析得到链接和歌曲信息
def analyze_ls(ipt):
    ipt=str(ipt)
    if 'a' in ipt:
        i=ipt.replace('a','')
        ls='/playlist/track/all'
        params={'id':i,'limit':10}
        data=json.loads(requests.get(api+ls,params=params,cookies=cookies).text)['songs']
        uid=[]
        for d in data:
            uid.append(str(d['id']))
        uid=','.join(uid)
    if ',' in ipt:
        uid=ipt
    params={'id':uid,'level':'exhigh'}
    params1={'ids':uid}
    namels=[]
    ss=json.loads(requests.get(api+'/song/detail',params=params1,cookies=cookies).text)['songs']
    ##uu=
    for s,u in zip(ss,uid.split(',')):
        params={'id':u,'level':'exhigh'}
        url=json.loads(requests.get(api+'/song/url/v1',params=params,cookies=cookies).text)['data'][0]['url']
        if url==None:
            url='https://ghproxy.com/https://github.com/wzk0/photo/blob/0158be3de27768ae455066eaa21c8b10540ce79e/Never%20Gonna%20Give%20You%20Up%20-%20Rick%20Astley.mp3?raw=true'
        else:
            url=url
        namels.append({'name':s['name'],'url':url,'artist':get_ar(s['ar']),'cover':s['al']['picUrl']})
    return namels

##歌词美化
def beautjson(d):
    lrc=d['lrc']['lyric']
    llrc=[]
    for lr in lrc.split('\n'):
        llrc.append(lr.split(']')[-1])
    return llrc

def analyze_10(data):
    ar=[]
    for a in data['result']['albums']:
        ar.append({'title':a['name']+' - '+get_ar(a['artists']),'year':a['idStr'],'link':a['picUrl'],'word':'跳转至专辑封面⚡️'})
    return ar

def analyze_100(data):
    ar=[]
    for a in data['result']['artists']:
        ar.append({'title':a['name'],'year':a['id'],'link':a['picUrl'],'word':'跳转至歌手头像⚡️'})
    return ar

def analyze_1000(data):
    ar=[]
    for a in data['result']['playlists']:
        ar.append({'title':a['name']+' - 🎉来自用户: %s创建 - '%a['creator']['nickname']+'播放次数: %s'%str(a['playCount']),'year':str(a['id']),'link':'/ls/a%s'%str(a['id']),'word':'跳转至歌单播放界面⚡️'})
    return ar

##以下是视图函数

@app.route('/')
def hello():
    try:
        return render_template('index.html',name='Thdbd')
    except:
        return render_template('404.html'),404

@app.route('/about')
def abt():
    try:
        return render_template('about.html')
    except:
        return render_template('404.html'),404

@app.route('/hot')
def hot():
    try:
        global api
        hot='/search/hot/detail'
        global cookies
        r=requests.get(api+hot,cookies=cookies).text
        ls=json.loads(r)['data']
        ll=[]
        for l in ls:
            ll.append({'title': l['searchWord'], 'year': l['score']})
    except:
        return render_template('404.html'),404
    return render_template('hot.html',name='Thdbd',movies=ll)

##搜索的静态页面
@app.route('/search',methods=['GET','POST'])
def ss():
    try:
        global api
        if request.method == 'POST':
            title=request.form.get('title')
            try:
                year=request.form.get('year')
            except:
                year='50'
            typ=request.form.get('typ')
            if typ=='':
                r=api+'/cloudsearch?'+'keywords='+title+'&limit='+year
            else:
                r=api+'/cloudsearch?'+'keywords='+title+'&limit='+year+'&type='+typ
            return redirect(url_for('res',movies=r))
    except:
        return render_template('404.html'),404
    return render_template('search.html')

@app.route('/result/<path:movies>')
def res(movies):
    try:
        global cookies
        r=requests.get(movies,cookies=cookies)
        if '&type=1000' in str(r.url):
            movies=analyze_1000(json.loads(r.text))
        else:
            if '&type=100' in str(r.url):
                movies=analyze_100(json.loads(r.text))
            else:
                if '&type=10' in str(r.url):
                    movies=analyze_10(json.loads(r.text))
                else:
                    movies=analyze(json.loads(r.text))
    except:
        return render_template('404.html'),404
    return render_template('result.html',movies=movies)

@app.route('/download',methods=['GET','POST'])
def download():
    try:
        global api
        if request.method == 'POST':
            title=request.form.get('title')
            return redirect(url_for('dl',uid=title))
    except:
        return render_template('404.html'),404
    return render_template('download.html')

@app.route('/dl/<int:uid>')
def dl(uid):
    try:
        global api
        global cookies
        dl='/song/url/v1'
        params={'id':uid,'level':'exhigh'}
        url=json.loads(requests.get(api+dl,params=params,cookies=cookies).text)['data'][0]['url']
        if url==None:
            url='https://ghproxy.com/https://github.com/wzk0/photo/blob/0158be3de27768ae455066eaa21c8b10540ce79e/Never%20Gonna%20Give%20You%20Up%20-%20Rick%20Astley.mp3?raw=true'
        else:
            url=url
        lrc=beautjson(json.loads(requests.get(api+'/lyric?id='+str(uid),cookies=cookies).text))
        movies=json.loads(requests.get(api+'/song/detail?ids='+str(uid),cookies=cookies).text)
        name=movies['songs'][0]['name']
        ar=[]
        for a in movies['songs'][0]['ar']:
            ar.append(a['name'])
        pic=movies['songs'][0]['al']['picUrl']
        namels=[name,','.join(ar),pic]
    except:
        return render_template('404.html'),404
    return render_template('play.html',url=url,lrc=lrc,namels=namels)

@app.route('/list',methods=['GET','POST'])
def list():
    try:
        global api
        if request.method == 'POST':
            title=request.form.get('title')
            return redirect(url_for('ls',uid=title))
    except:
        return render_template('404.html'),404
    return render_template('list.html')

@app.route('/ls/<string:uid>')
def ls(uid):
    try:
        return render_template('ls.html',ls=analyze_ls(uid))
    except:
        return render_template('404.html'),404

@app.errorhandler(404)
def pnf(e):
    return render_template('404.html'),404

if __name__ == "__start__":
    app.run(host='0.0.0.0',port=80)