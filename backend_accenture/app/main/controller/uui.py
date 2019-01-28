from flask import Flask, request
import requests
import json

app = Flask(__name__)

#@app.route('/getUUI', methods=['GET'])

callid = "21994309366@192.168.50.202"

def getUUI(callid):
    r = requests.post("http://18.228.148.116:8086/pavirtual", data={'callid': callid})
     #data = json.loads(r.content)
    # data = request.body
    # resp =data.get('uui')
    # print(r.content.decode('UTF-8'))
   
    data = {"uui": r.content.decode('UTF-8') }
    print(data['uui']) 
    
    return r

getUUI(callid)


