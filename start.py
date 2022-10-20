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

def analyze(dic):
    ls=[]
    for l in dic['result']['songs']:
        ar=[]
        for ll in l['ar']:
            ar.append(ll['name'])
        d={'title':l['name']+' - '+','.join(ar),'year':str(l['id'])}
        ls.append(d)
    return ls

def beautjson(d):
    lrc=d['lrc']['lyric']
    llrc=[]
    for lr in lrc.split('\n'):
        llrc.append(lr.split(']')[-1])
    return llrc

@app.route('/')
def hello():
    return render_template('index.html',name='Thdbd')

@app.route('/hot')
def hot():
    global api
    hot='/search/hot/detail'
    global cookies
    r=requests.get(api+hot,cookies=cookies).text
    ls=json.loads(r)['data']
    ll=[]
    for l in ls:
        ll.append({'title': l['searchWord'], 'year': l['score']})
    return render_template('hot.html',name='Thdbd',movies=ll)

@app.route('/search',methods=['GET','POST'])
def ss():
    global api
    if request.method == 'POST':
        title=request.form.get('title')
        year=request.form.get('year')
        ss='/cloudsearch'
        params={'keywords':title,'limit':year}
        global cookies
        r=requests.get(api+ss,params=params,cookies=cookies)
        return redirect(url_for('res',movies=r.url))
    return render_template('search.html')

@app.route('/result/<path:movies>')
def res(movies):
    global cookies
    r=requests.get(movies,cookies=cookies)
    movies=analyze(json.loads(r.text))
    return render_template('result.html',movies=movies)

@app.route('/download',methods=['GET','POST'])
def download():
    global api
    if request.method == 'POST':
        title=request.form.get('title')
        return redirect(url_for('dl',uid=title))
    return render_template('download.html')

@app.route('/dl/<int:uid>')
def dl(uid):
    global api
    global cookies
    dl='/song/url/v1'
    params={'id':uid,'level':'higher'}
    url=json.loads(requests.get(api+dl,params=params,cookies=cookies).text)['data'][0]['url']
    lrc=beautjson(json.loads(requests.get(api+'/lyric?id='+str(uid),cookies=cookies).text))
    movies=json.loads(requests.get(api+'/song/detail?ids='+str(uid),cookies=cookies).text)
    name=movies['songs'][0]['name']
    ar=[]
    for a in movies['songs'][0]['ar']:
        ar.append(a['name'])
    pic=movies['songs'][0]['al']['picUrl']
    namels=[name,','.join(ar),pic]
    return render_template('play.html',url=url,lrc=lrc,namels=namels)

@app.errorhandler(404)
def pnf(e):
    return render_template('404.html'),404

if __name__ == "__start__":
    app.run(host='0.0.0.0',port=80)