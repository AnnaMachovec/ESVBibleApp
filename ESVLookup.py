import sys
import requests
from flask import Flask
from flask import render_template
from flask import request

from flask import Flask, redirect, url_for, request
app = Flask(__name__)
API_KEY = 'd5d62edc057317ae013dad4821eb7524fb5b4045'
API_URL = 'https://api.esv.org/v3/passage/text/'

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
        return redirect(url_for('get_esv_text',passage = message))
        #displaytext = get_esv_text(message)
    else:
        return render_template('login.html', message=message)
    #return message
#...


app.run(host='localhost', port=5000)
