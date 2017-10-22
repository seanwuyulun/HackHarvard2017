from flask import Flask, request, jsonify, redirect, url_for, flash
import json
import matplotlib.pyplot as plt
from subprocess import Popen, PIPE
from threading import Thread
import time
import StringIO, base64
from urllib import quote
import requests
 
app = Flask(__name__)
 
values = []

imgdata = StringIO.StringIO()

def getSI():
    global values
    global imgdata
    counter = 1
    while True:
        p = Popen('iw dev wlp3s0 station dump'.split(' '), stdout=PIPE)
        values.append(int(p.stdout.readlines()[8][11:14]))
        if len(values) > 10000:
            values = values[len(values)-10000:]
        counter += 1
        counter = counter % 20
        if counter == 0:
            plt.scatter(range(len(values)), values)
            fig = plt.gcf()
            fig.savefig(imgdata, format='png')
            imgdata.seek(0)
 
 
@app.route('/',methods=['GET'])
def wifindr():
    global imgdata
    confidence = json.loads(requests.get('http://35.199.177.109:8888/heh').content)
    
    resp = jsonify({'name':['David', 'Saarthak', 'Sean'][confidence.index(max(confidence))], 'confidence': confidence, 'image':'data:image/png;base64,'+quote(base64.b64encode(imgdata.buf))})
    resp.headers['Content-type:'] = 'application/json'
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp

if __name__ == '__main__':
    background_thread = Thread(target=getSI)
    background_thread.start()
    app.run(host='0.0.0.0', port=8080)

