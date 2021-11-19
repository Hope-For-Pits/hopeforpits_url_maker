import qrcode

urllist = open('site_urls.csv','r').readlines()

for url in urllist:
    url = url.rstrip()    
    img = qrcode.make(url)
    name = url.split('/')[-1]
    print("{name},{url}".format(name=name,url=url))
    img.save('static/qrcodes/site/' + name.rstrip() + '.png')
    img.close()
             
