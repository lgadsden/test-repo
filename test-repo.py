#!/usr/bin/env python

# the part up top tells the computer to use python  
# (while the app is technially serveless) since we do not manage a server ourselves
# A server is started byb Heroku and the bit above tells it to use python to run this code 

# Here we import the packages needed for app 
import boto3
import urllib
import json
import os
# Here we import specific modules that we want to use from Flask
from flask import Flask 
from flask import request
from flask import make_response

dynamodb = boto3.resource('dynamodb', region_name = 'us-east-1', aws_access_key_id= os.environ['ACCESS_KEY'],
    aws_secret_access_key= os.environ['SECRET_KEY'])

table = dynamodb.Table('chatbot_info')

# Flask app should start in global layout
app = Flask(__name__)

# This is needed to beging Flask app --- POST is a method for transmitting data 
@app.route('/webhook', methods=['POST'])
def webhook():
    # api.ai pushes json info to the app's url and req grabs the json 
    req = request.get_json(silent=True, force=True)
    # all of the req.get instances pull data fromm specific variables from the json
    id1 = req.get('id')
    sessionId = req.get("sessionId")
    timestamp = req.get("timestamp")
    result = req.get("result")
    query = result.get("resolvedQuery")
    fulfillment = result.get('fulfillment')
    
    plus = {'id' = id1,
           'sessionId': sessionId,
           'timestamp': timestamp,
           'result': result,
           'query' : query
           'fulfillment': fulfillment}
    
    table.put_item(Item = plus)
    
        

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
