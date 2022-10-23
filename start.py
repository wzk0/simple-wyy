from flask import Flask,render_template,request,redirect,url_for
import requests
import json
import random

session=requests.Session()

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
    global session
    global api
    global cookies  
    ipt=str(ipt)
    if 'a' in ipt:
        i=ipt.replace('a','')
        pls=json.loads(session.get(api+'/playlist/detail?id='+i).text)['playlist']
        if pls['description']==None:
            description=str(i)+' - 😶‍🌫️这张歌单没有描述...'
        else:
            description=pls['name']+' - '+pls['description']
        word=description
        ls='/playlist/track/all'
        params={'id':i,'limit':20}
        data=json.loads(session.get(api+ls,params=params,cookies=cookies).text)['songs']
        uid=[]
        for d in data:
            uid.append(str(d['id']))
        uid=','.join(uid)
    if 'b' in ipt:
        i=ipt.replace('b','')
        ls='/album?id=%s'%i
        data=json.loads(session.get(api+ls,cookies=cookies).text)['songs']
        word=data[0]['al']['name']
        uid=[]
        for i in data:
            uid.append(str(i['id']))
        uid=','.join(uid)
    if ',' in ipt:
        uid=ipt
        word='自定义歌单 - 😘恭喜你发现本站最强大的功能,说明你已经是高手啦!'
    params={'id':uid,'level':'exhigh'}
    params1={'ids':uid}
    namels=[]
    ss=json.loads(session.get(api+'/song/detail',params=params1,cookies=cookies).text)['songs']
    for s,u in zip(ss,uid.split(',')):
        params={'id':u,'level':'exhigh'}
        url=json.loads(session.get(api+'/song/url/v1',params=params,cookies=cookies).text)['data'][0]['url']
        if url==None:
            url='https://ghproxy.com/https://github.com/wzk0/photo/blob/0158be3de27768ae455066eaa21c8b10540ce79e/Never%20Gonna%20Give%20You%20Up%20-%20Rick%20Astley.mp3?raw=true'
        else:
            url=url
        namels.append({'name':s['name'],'url':url,'artist':get_ar(s['ar']),'cover':s['al']['picUrl']})
    return namels,word

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
        ar.append({'title':a['name']+' - '+get_ar(a['artists']),'year':str(a['id']),'link':'/ls/b%s'%str(a['id']),'word':'跳转至专辑播放界面⚡️'})
    return ar

def analyze_100(data):
    ar=[]
    for a in data['result']['artists']:
        ar.append({'title':a['name'],'year':str(a['id']),'link':'/singer/%s'%str(a['id']),'word':'跳转至歌手页面⚡️'})
    return ar

def analyze_1000(data):
    ar=[]
    for a in data['result']['playlists']:
        ar.append({'title':a['name']+' - 🎉来自用户: %s创建 - '%a['creator']['nickname']+'播放次数: %s'%str(a['playCount']),'year':str(a['id']),'link':'/ls/a%s'%str(a['id']),'word':'跳转至歌单播放界面⚡️'})
    return ar

def analyze_1002(data):
    ar=[]
    for a in data['result']['userprofiles']:
        ar.append({'title':a['nickname'],'year':str(a['userId']),'link':'/me/%s'%str(a['userId']),'word':'查看Ta的歌单⚡️'})
    return ar

def me(data):
    ar=[]
    for a in data:
        if a['description']==None:
            description='😶‍🌫️这张歌单没有描述...'
        else:
            description=a['description']
        ar.append({'description':description,'listname':a['name'],'musicsize':str(a['trackCount']),'playcount':str(a['playCount']),'listid':str(a['id']),'link':'/ls/a%s'%str(a['id']),'word':'跳转至歌单播放界面⚡️'})
    vip=str(data[0]['creator']['vipType'])
    creator=data[0]['creator']['nickname']
    avatar=data[0]['creator']['avatarUrl']
    description=data[0]['creator']['description']
    if description=='':
        description='😶‍🌫️这位用户没有描述...'
    return ar,vip,creator,avatar,description

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
    global session
    global api
    global cookies  
    try:        
        hot='/search/hot/detail'        
        r=session.get(api+hot,cookies=cookies).text
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
        if request.method == 'POST':
            title=request.form.get('title')
            year=request.form.get('year')
            if year=='':
                year='50'
            else:
                year=year
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
    global session
    global api
    global cookies  
    try:
        if 'cloudsearch?keywords=' not in movies:
            return render_template('404.html'),404
        else:
            r=session.get(movies,cookies=cookies)
        if '&type=1002' in str(r.url):
            movies=analyze_1002(json.loads(r.text))
        else:
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
        return render_template('result.html',movies=movies)
    except:
        return render_template('404.html'),404

@app.route('/download',methods=['GET','POST'])
def download():
    try:        
        if request.method == 'POST':
            title=request.form.get('title')
            return redirect(url_for('dl',uid=title))
    except:
        return render_template('404.html'),404
    return render_template('download.html')

@app.route('/dl/<int:uid>')
def dl(uid):
    global session
    global api
    global cookies  
    try:                
        dl='/song/url/v1'
        params={'id':uid,'level':'exhigh'}
        url=json.loads(session.get(api+dl,params=params,cookies=cookies).text)['data'][0]['url']
        if url==None:
            url='https://ghproxy.com/https://github.com/wzk0/photo/blob/0158be3de27768ae455066eaa21c8b10540ce79e/Never%20Gonna%20Give%20You%20Up%20-%20Rick%20Astley.mp3?raw=true'
        else:
            url=url
        lrc=beautjson(json.loads(session.get(api+'/lyric?id='+str(uid),cookies=cookies).text))
        movies=json.loads(session.get(api+'/song/detail?ids='+str(uid),cookies=cookies).text)
        al_ls={'id':movies['songs'][0]['al']['id'],'name':movies['songs'][0]['al']['name']}
        name=movies['songs'][0]['name']
        ar=[]
        for a in movies['songs'][0]['ar']:
            ar.append(a['name'])
        ar_id=[]
        for a in movies['songs'][0]['ar']:
            ar_id.append(str(a['id']))
        arar=[]
        for n,i in zip(ar,ar_id):
            arar.append({'name':n,'id':i})
        pic=movies['songs'][0]['al']['picUrl']
        namels=[name,','.join(ar),pic]
        return render_template('play.html',url=url,lrc=lrc,namels=namels,al_ls=al_ls,arar=arar) 
    except:
        return render_template('404.html'),404
    return render_template('play.html',url=url,lrc=lrc,namels=namels,al_ls=al_ls,arar=arar) 

@app.route('/list',methods=['GET','POST'])
def list():
    try:        
        if request.method == 'POST':
            title=request.form.get('title')
            return redirect(url_for('ls',uid=title))
    except:
        return render_template('404.html'),404
    return render_template('list.html')

@app.route('/singer/<string:uid>')
def singer(uid):
    global session
    global api
    global cookies  
    try:        
        r=json.loads(session.get(api+'/artists?id='+uid).text)
        hotsongs=[]
        for h in r['hotSongs']:
            hotsongs.append({'name':h['name']+' - '+get_ar(h['ar']),'uid':str(h['id'])})
        ls={'name':r['artist']['name'],'alias':','.join(r['artist']['alias']),'bio':r['artist']['briefDesc'],'picUrl':r['artist']['picUrl'],'musicsize':str(r['artist']['musicSize']),'songs':hotsongs}
        return render_template('singer.html',res=ls)
    except:
        return render_template('404.html'),404

@app.route('/ls/<string:uid>')
def ls(uid):
    try:
        ls,word=analyze_ls(uid)
        return render_template('ls.html',ls=ls,word=word)
    except:
        return render_template('404.html'),404

@app.route('/star')
def rand():
    global session
    global api
    global cookies  
    try:        
        cat_ls=['综艺', '流行', '影视原声', '华语', '清晨', '怀旧', '夜晚', '摇滚', '欧美', '清新', 'ACG', '浪漫', '民谣', '日语', '学习', '儿童', '电子', '韩语', '校园', '工作', '午休', '伤感', '粤语', '游戏', '舞曲', '说唱', '70后', '治愈', '下午茶', '放松', '轻音乐', '80后', '地铁', '90后', '孤独', '驾车', '爵士', '感动', '乡村', '网络歌曲', '运动', '兴奋', 'KTV', 'R&B/Soul', '旅行', '古典', '快乐', '经典', '散步', '民族', '翻唱', '酒吧', '安静', '吉他', '英伦', '思念', '金属', '钢琴', '器乐', '朋克', '蓝调', '榜单', '00后', '雷鬼', '世界音乐', '拉丁', 'New Age', '古风', '后摇', 'Bossa Nova']
        cat=random.choice(cat_ls)
        params={'limit':10,'cat':cat}
        r=json.loads(session.get(api+'/top/playlist',params=params).text)['playlists']
        try:
            ti=json.loads(session.get('http://quan.suning.com/getSysTime.do').text)['sysTime2'].split(' ')[0].split('-')
            day=ti[0]+'年'+ti[1]+'月'+ti[2]+'日'
        except:
            day='今天'
        ls=[]
        for rr in r:
            ls.append({'name':rr['name'],'uid':str(rr['id']),'description':rr['description']})
        return render_template('star.html',cat=cat,res=ls,day=day)
    except:
        return render_template('404.html'),404

@app.route('/me/<string:uuid>')
def mme(uuid):
    try:
        global session
        global api
        global cookies 
        ar,vip,creator,avatar,description=me(json.loads(session.get(api+'/user/playlist?uid='+str(uuid),cookies=cookies).text)['playlist'])
        return render_template('me.html',ar=ar,vip=vip,creator=creator,avatar=avatar,description=description)
    except:
        return render_template('404.html'),404

@app.route('/mine',methods=['GET','POST'])
def mine():
    try:        
        if request.method == 'POST':
            title=request.form.get('title')
            return redirect(url_for('me',uuid=title))
    except:
        return render_template('404.html'),404
    return render_template('mine.html')

@app.errorhandler(404)
def pnf(e):
    return render_template('404.html'),404

if __name__ == "__start__":
    app.run(host='0.0.0.0')