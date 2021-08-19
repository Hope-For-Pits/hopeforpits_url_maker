import subprocess
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
curlcommand = """curl -s 'https://airtable.com/v0.3/table/tblb028UTUaTbH8TE/getRowsMatchingName' \
  -H 'Connection: keep-alive' \
  -H 'Pragma: no-cache' \
  -H 'Cache-Control: no-cache' \
  -H 'sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"' \
  -H 'DNT: 1' \
  -H 'x-time-zone: America/New_York' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'x-airtable-page-load-id: pglxfFP5GMO6tnD4r' \
  -H 'x-airtable-application-id: appFN3sh7XBSEoYHt' \
  -H 'ot-tracer-sampled: true' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36' \
  -H 'x-airtable-inter-service-client: webClient' \
  -H 'ot-tracer-traceid: 28fd0e6c5855e778' \
  -H 'Accept: application/json, text/javascript, */*; q=0.01' \
  -H 'x-airtable-inter-service-client-code-version: 62d524ac8f5a360c12823a4941c191e60f3313c8' \
  -H 'x-user-locale: en' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'ot-tracer-spanid: 53d12b1d063a7229' \
  -H 'Origin: https://airtable.com' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Cookie: brw=brwrrLG5K7xfpdeBA; optimizelyEndUserId=oeu1626128817776r0.18929413231649161; 8gma29=1; _ga=GA1.2.1700923836.1626128819; amplitude_idairtable.com=eyJkZXZpY2VJZCI6IjY1MTYxZGZkLTYxMGEtNGU3OC05NTNkLWQ1YWJjYWRkMDU5ZFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTYyNjEyODgxOTIyNywibGFzdEV2ZW50VGltZSI6MTYyNjEyODgxOTIzOCwiZXZlbnRJZCI6MSwiaWRlbnRpZnlJZCI6Miwic2VxdWVuY2VOdW1iZXIiOjN9; _mkto_trk=id:458-JHQ-131&token:_mch-airtable.com-1626128819706-51359; _fbp=fb.1.1626128819751.754215499; intercom-id-wb1whb4b=bd26e1ad-7f95-4bd9-9594-8da4b38ac37d; fs_uid=rs.fullstory.com#113G8Y#5043310136336384:5561862677274624/1657664834; phg=0; __Host-airtable-session=eyJzZXNzaW9uSWQiOiJzZXNjMXlKV1pYd3ZjVDZYYSIsImNzcmZTZWNyZXQiOiI2a2JLdC1nTU9SX0pOeElXcE1pWV9paGMiLCJoaWdoU2VjdXJpdHlNb2RlRW5hYmxlZFRpbWUiOjE2MjYxMjg4NDIwNDcsInVzZXJJZCI6InVzcmJXa3BQaHd1eHBqZERZIn0=; __Host-airtable-session.sig=gGtcA0sFR2S5Ve9hP1vV0pKA3V2ICeO1XRmxSTJYqGY; __zlcmid=152kAtF5EOOcxN5; AWSELB=F5E9CFCB0C87D62DB5D03914FDC2A2D2D45FBECE92075869B3F7F698D732FCC7347AFF1CEA0BC1262B9940A7DF1D234855648842F3FE238CDB5BAF086C42E42BDECC69CACA; AWSELBCORS=F5E9CFCB0C87D62DB5D03914FDC2A2D2D45FBECE92075869B3F7F698D732FCC7347AFF1CEA0BC1262B9940A7DF1D234855648842F3FE238CDB5BAF086C42E42BDECC69CACA; lightstep_guid%2FsharedViewOrApp=61c28f784874ee26; lightstep_session_id=12a8ac782e3c1716; mv=eyJzdGFydFRpbWUiOiIyMDIxLTA4LTE5VDAxOjQzOjM4LjIxNVoiLCJsb2NhdGlvbiI6Imh0dHBzOi8vYWlydGFibGUuY29tL3NocjczZWIqKioqKioqKioqIiwiaW50ZXJuYWxUcmFjZUlkIjoidHJjdllwOUY0WWE0M3JmMEEifQ==; mbpg=2022-08-19T01:54:52.654ZusrbWkpPhwuxpjdDYpro; mbpg.sig=lwJHtqRY4lquLEOsfxsBtazvajr0W_7mMtuJxdeQUfI' \
  --data-raw 'stringifiedObjectParams=%7B%22rowName%22%3A%22%22%2C%22limit%22%3A1000%2C%22offset%22%3A0%2C%22columnLimit%22%3A7%2C%22rowIdsToIgnore%22%3A%5B%5D%2C%22viewIdForRecordSelection%22%3A%22viwo2LKvCNjeIMqG4%22%2C%22includeColumnData%22%3Atrue%2C%22returnOnlyPrimaryColumn%22%3Atrue%7D&requestId=reqkE3BNeQi6cdllP&accessPolicy=%7B%22allowedActions%22%3A%5B%7B%22modelClassName%22%3A%22view%22%2C%22modelIdSelector%22%3A%22viwSDbNSkuMSt0jxT%22%2C%22action%22%3A%22readSharedFormData%22%7D%2C%7B%22modelClassName%22%3A%22view%22%2C%22modelIdSelector%22%3A%22viwSDbNSkuMSt0jxT%22%2C%22action%22%3A%22submitSharedForm%22%7D%2C%7B%22modelClassName%22%3A%22application%22%2C%22modelIdSelector%22%3A%22appFN3sh7XBSEoYHt%22%2C%22action%22%3A%22createAttachmentUploadS3Policies%22%7D%2C%7B%22modelClassName%22%3A%22table%22%2C%22modelIdSelector%22%3A%22tblb028UTUaTbH8TE%22%2C%22action%22%3A%22getRowsMatchingName%22%2C%22actionArguments%22%3A%7B%22returnOnlyPrimaryColumn%22%3Atrue%2C%22viewIdForRecordSelection%22%3A%22viwo2LKvCNjeIMqG4%22%7D%7D%2C%7B%22modelClassName%22%3A%22table%22%2C%22modelIdSelector%22%3A%22tblb028UTUaTbH8TE%22%2C%22action%22%3A%22readDataForRowCards%22%2C%22actionArguments%22%3A%7B%22returnOnlyPrimaryColumn%22%3Atrue%7D%7D%5D%2C%22shareId%22%3A%22shrL8Ozj2HE2G8LEO%22%2C%22applicationId%22%3A%22appFN3sh7XBSEoYHt%22%2C%22sessionId%22%3A%22sesc1yJWZXwvcT6Xa%22%2C%22generationNumber%22%3A0%2C%22signature%22%3A%22a323d2dc7a46804fdadca53597dafc6645e856d9b60c22556e36fb7ccead4e75%22%7D' \
  --compressed
"""

urlbase = 'https://airtable.com/shrL8Ozj2HE2G8LEO?prefill_Which+dog+are+you+applying+for?='

@app.route('/')
def index():
    html = """
    <h1>Hope For Pits URL Maker</h1>
    <h2>new method (ultra janky)</h2>
    <p>Just wait for a second, the textarea is already prepopulated with the json. 
        what makes this work is incredibly janky and I imagine that it probably needs
        to be refreshed every day, but it's working as of now. Yes, I probably should 
        just make it all happen in the background, but for some reason adding a new api
        endpoint and calling it from javascript seemed like the thing to do.</p>
    <p>if you think this sucks, keep it to yourself, or bother me, idc.</p>
    <h2>old method</h2>
    <p>To use the url maker you'll need to use chrome developer tool, if you're running chrome you can open with F12.</p>
    <p>Here's <a href="https://developer.chrome.com/docs/devtools/open/">a tutorial</a> on chrome dev tools if you're curious.</p>
    <p>Use chrome dev tools on <a href="https://airtable.com/shrL8Ozj2HE2G8LEO" target="_blank">adoption application page</a> to retrieve the response from GetRowsMatchingName GET request and paste it here.</p>
    <p>it will look something like this:</p>
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
    """
    return html

@app.route("/get/curl")
def get_curl():
    status, output = subprocess.getstatusoutput(curlcommand)
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
