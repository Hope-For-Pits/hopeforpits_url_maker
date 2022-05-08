from pprint import pprint
from docxtpl import DocxTemplate
import os
from datetime import datetime

def fixpd(fieldname, series):
    return series[fieldname].to_string().split(' ')[-1]

def generate_doc(data):
    # pprint(data)
    c = {}
    doc = DocxTemplate('hope-for-pits-adoption-contract-tpl.docx')
    
    c['name'] = data['Applicant Name']
    c['phone'] = data['Phone']
    c['email'] = data['Email']
    c['address'] = data['Address']
    petdata = data['petdata']
    c['gender'] = fixpd('gender',petdata)
    c['petname'] = fixpd('name',petdata)
    c['altered'] = fixpd('altered',petdata)
    c['petdob'] = fixpd('estimated_birth_date',petdata)
    c['color'] = fixpd('color',petdata)
    fname = os.path.join('./static/contracts/',c['petname'] + '_' + datetime.strftime(datetime.now(),'%s') + '.docx')    
    try:
        doc.render(c)
        doc.save(fname)
        return fname
    except Exception as e:
        print(e)
        return False    
    