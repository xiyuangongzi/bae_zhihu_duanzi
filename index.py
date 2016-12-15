#-*- coding:utf-8 -*-
from flask import Flask,render_template
from tinydb import TinyDB, where

app = Flask(__name__)
url = ''
@app.route('/')
def index():
    conte = TinyDB('/home/bae/app/conte.json')
    content = conte.all()
    return render_template('index.html',conte=content)

#app.run(debug=True)

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
