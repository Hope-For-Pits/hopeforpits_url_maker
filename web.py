import os, zlib, base64, subprocess
import cryptocode
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

curlcommand = "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*+ogdWOKs8LlLsFbGrm6vnw==*1mHfn06LW1A37XU5/wS0Gw==*YJSrDbyh80Eux1aWJhJLfw=="
key = os.environ['CURL_KEY']
curldec = cryptocode.decrypt(curlcommand,key)
curlcmd = zlib.decompress(base64.b64decode(curldec)).decode()

urlbase = 'https://airtable.com/shrL8Ozj2HE2G8LEO?prefill_Which+dog+are+you+applying+for?='

@app.route('/')
def index():
    html = """
    <html>
        <head>            
            <link rel="stylesheet" href="https://unpkg.com/bootstrap@4.1.1/dist/css/bootstrap.css">
        </head>
        <body>          
            <div class="container">  
                <h1>Hope For Pits URL Maker</h1>
                <h2>new method (ultra janky)</h2>
                <p>Just load the page and the textarea is already prepopulated with the json. 
                    what makes this work is incredibly janky and I imagine that it probably needs
                    to be refreshed every day, but it's working as of now. Yes, I probably should 
                    just make it all happen in the background, but for some reason adding a new api
                    endpoint and calling it from javascript seemed like the thing to do.</p>
                <p>if you think this sucks, keep it to yourself, or bother me, idc.</p>
                <h2>old method</h2>
                <p>To use the url maker you'll need to use chrome developer tool, if you're running 
                    chrome you can open with F12. Here's 
                    <a href="https://developer.chrome.com/docs/devtools/open/">a tutorial</a> on chrome 
                    dev tools if you're curious.</p>
                <p>Use chrome dev tools on <a href="https://airtable.com/shrL8Ozj2HE2G8LEO" target="_blank">
                    adoption application page</a> to retrieve the response from GetRowsMatchingName GET request
                    and paste it here. It will look something like this:</p>
                <pre>{"msg":"SUCCESS","data":{"rowResults":[{"id":"recAQBiyRQVOpUUai","createdTime":"2021-07-07T18:53:31.000Z","cellValuesByColumnId":{"fldk63tdzoGOMN8JR":"Brandon"}}...</pre>
                <form action="/make_urls" method="post">
                    <label>Pet list JSON</label>
                    <br />
                    <textarea id="petlisttextarea" name="petlist" style="width:600px; height:300px;"></textarea>
                    <p><input type="submit" value="submit"></p>
                </form>
                <script type="text/javascript">
                fetch("/get/curl",{
                    method: "GET"
                }).then(response => response.json())
                .then(data => document.getElementById("petlisttextarea").value = JSON.stringify(data))
                </script>            
            </div>
        </body>
    </html>
    
    """
    return html

@app.route("/get/curl")
def get_curl():
    status, output = subprocess.getstatusoutput(curlcmd)
    del status
    return output

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
