#!/usr/bin/env python3

import qrcode
import json
import os
import sys

errmsg="""
Need json file containing GET response of list of dogs
To get this file, save the results of the GET request from https://airtable.com/v0.3/table/<your table id>/getRowsMatchingName
I collected this using chrome dev tools and clicking the "Add" button on the adoption page
and then by copying and pasting the response to a file at "dogs.json"
"""

if not os.path.exists('dogs.json'):
    print(errmsg)
    sys.exit(1)
if not os.path.isdir('qrcodes'):
    os.mdkir('qrcodes')

ddata = json.loads(open('dogs.json','r').read())
urlbase = 'https://airtable.com/shrL8Ozj2HE2G8LEO?prefill_Which%20dog%20are%20you%20applying%20for?='
urllist = open('urllist.csv','w')
urllist.write('name,id,url\n')

for dog in ddata['data']['rowResults']:
    id = dog['id']
    name = dog['cellValuesByColumnId']['fldk63tdzoGOMN8JR']
    url = urlbase + id
    print(name + ',' + url)
    urllist.write(name + ',' + id + ',' + url + '\n')
    img = qrcode.make(url)
    img.save('qrcodes/' + name + '.png')
    img.close()
    
urllist.close()


