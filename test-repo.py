#!/usr/bin/env python

# the part up top tells the computer to use python  
# (while the app is technially serveless) since we do not manage a server ourselves
# A server is started by Heroku and the bit above tells it to use python to run this code 

# Here we import the packages needed for app 
import boto3 #for aws 
import urllib
import json
import os
# Here we import specific modules that we want to use from Flask
from flask import Flask 
from flask import request
from flask import make_response

# sets credentials for using dynamodb under our account
dynamodb = boto3.resource('dynamodb', region_name = 'us-east-1', aws_access_key_id= os.environ['ACCESS_KEY'],
    aws_secret_access_key= os.environ['SECRET_KEY'])

# links to the chatbot table on dynamodb
table = dynamodb.Table('chatbot_info')

# Flask app should start in global layout
app = Flask(__name__)

# This is needed to begin the Flask app --- POST is a method for transmitting data 
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
    resp = fulfillment.get('speech')
    
    # we add the info that we want to a python dictionary
    plus = {'id' : id1,
           'sessionId': sessionId,
           'timestamp': timestamp,
           #'result': result,
           'query' : query,
           'response': resp}
    
    # we print the dictonary --- this can be viewed in the logs file
    print(plus)
    
    # we push items into the database
    return table.put_item(Item = plus)
    
        
# this was part of the default setup 
# if __name__ = 'main' runs the function this only if the file is called and not part of another module
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    # this just prints the port to the log file
    print "Starting app on port %d" % port
    
    # this runs the flask app  
    app.run(debug=True, port=port, host='0.0.0.0')
