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

# I'm sure this won't last more than an hour or so

cc = open('curl_command.sh','r')
curlcommand = cc.read()
cc.close()

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
