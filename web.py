from flask import Flask
from flask import request
from flask import send_file
from flask import render_template
import json
import qrcode
import zipfile
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

urlbase = 'https://airtable.com/shrL8Ozj2HE2G8LEO?prefill_Which+dog+are+you+applying+for?='

@app.route('/')
def index():
    html = """
    <h1>Hope For Pits URL Maker</h1>
    <p>To use the url maker you'll need to use chrome developer tool, if you're running chrome you can open with F12.</p>
    <p>Here's <a href="https://developer.chrome.com/docs/devtools/open/">a tutorial</a> on chrome dev tools if you're curious.</p>
    <p>Use chrome dev tools on <a href="https://airtable.com/shrL8Ozj2HE2G8LEO" target="_blank">adoption application page</a> to retrieve the response from GetRowsMatchingName GET request and paste it here.</p>
    <p>it will look something like this:</p>
    <pre>{"msg":"SUCCESS","data":{"rowResults":[{"id":"recAQBiyRQVOpUUai","createdTime":"2021-07-07T18:53:31.000Z","cellValuesByColumnId":{"fldk63tdzoGOMN8JR":"Brandon"}}...</pre>
    <form action="/make_urls" method="post">
        <label>Pet list JSON</label>
        <br />
        <textarea name="petlist" style="width:600px; height:300px;"></textarea>
        <p><input type="submit" value="submit"></p>
    </form>    
    """
    return html

@app.route("/get/<filename>")
def get_file(filename):
    return send_file(filename)

@app.route("/make_urls", methods=["POST"])
def make_urls():

    urllist = open('urllist.csv','w')
    urllist.write('name,id,url\n')
    dt = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    zfilename = 'static/zips/hope-for-pits-qr-codes_' + dt + '.zip'
    zfile = zipfile.ZipFile(zfilename,'w')
    zfile_url = '/' + zfilename

    if request.method == 'POST':
        
        data = request.form['petlist']
        jdata = json.loads(data)
        petlist = []
        for dog in jdata['data']['rowResults']:
            id = dog['id']
            name = dog['cellValuesByColumnId']['fldk63tdzoGOMN8JR']
            url = urlbase + id
            
            urllist.write(name + ',' + id + ',' + url + '\n')
            img = qrcode.make(url)
            qrfname = 'static/qrcodes/' + name + '.png'
            qrurl = '/' + qrfname
            petlist.append({'name':name,'id':id,'url':url,'qrurl':qrurl})            
            img.save(qrfname)
            img.close()
            zfile.write(qrfname)

    urllist.close()
    zfile.write('urllist.csv')
    zfile.close()    
    return render_template('urls.html',petlist=petlist,zfile_url=zfile_url)

if __name__ == '__main__':
    Path('static/qrcodes').mkdir(parents=True,exist_ok=True)
    Path('static/zips').mkdir(parents=True,exist_ok=True)    
    app.run()
