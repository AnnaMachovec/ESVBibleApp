import sys
import requests
from flask import Flask
from flask import render_template
from flask import request
import json
#import json_extract

from flask import Flask, redirect, url_for, request,jsonify
app = Flask(__name__)
API_KEY = '21a820e340b343e22a67b98541c6d0727af729cf'
API_URL = ''
API_SEARCH = ''

@app.route('/searchword/<word>',methods=['post','get'])
def searchword_text(word):
    alltext = []
    params = {
    'q': word,
    #'page': i
    }
    headers = {
        'Authorization': 'Token %s' % API_KEY
    }
    response = requests.get(API_SEARCH, params=params, headers=headers)
    page_count = response.json()['total_pages']


    for i in range(1,page_count):
        params = {
        'q': word,
        'page': i,
        #'page-size': 20
        }
        headers = {
            'Authorization': 'Token %s' % API_KEY
        }
        response = requests.get(API_SEARCH, params=params, headers=headers)
        passages = response.json()['results']
        alltext.append(passages)



    print(alltext)



    #for page in range(1,1000):
    #assages = response.json()['next']

    #print(passages)

    #jspassages = jsonify(passages)
    #allpassages = ''
    #for obj in passages:
    #    part = ''
    #    if obj["reference"]:


    #return finalpassagetext
    return render_template('displayall.html',allpassages= alltext)

@app.route('/search/<passage>',methods=['post','get'])
def get_esv_text(passage):
    params = {
        'q': passage,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': False,
        'include-short-copyright': False,
        'include-passage-references': False
    }

    headers = {
        'Authorization': 'Token %s' % API_KEY
    }

    response = requests.get(API_URL, params=params, headers=headers)

    passages = response.json()['passages']
    finalpassageaddress = passage
    finalpassagetext = ''
    if passages:
        finalpassagetext = passages[0].strip()
    else:
        finalpassagetext='Passage does not exist!'
    #return finalpassagetext
    return render_template('display.html',message=finalpassagetext,address = finalpassageaddress)



@app.route('/search/', methods=['POST', 'GET'])
def login():
    message = ''
    if request.method == 'POST':
        message = request.form.get('esvref')  # access the data inside
        return redirect(url_for('searchword_text',word = message))
        #displaytext = get_esv_text(message)
    else:
        return render_template('login.html', message=message)
    #return message
#...


app.run(host='localhost', port=5000)
