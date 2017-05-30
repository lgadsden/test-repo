#!/usr/bin/env python

# the part up top tells the computer to use python  
# (while the app is technially serveless) since we do not manage a server ourselves
# A server is started byb Heroku and the bit above tells it to use python to run this code 

# Here we import the packages needed for app 
import urllib
import json
import os
# Here we import specific modules that we want to use from Flask
from flask import Flask 
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


# This is needed to beging Flask app --- POST is a method for transmitting data 
@app.route('/webhook', methods=['POST'])
def webhook():
    # api.ai pushes json info to the app's url and req grabs the json 
    req = request.get_json(silent=True, force=True)
    
    # all of the req.get instances pull data fromm specific variables from the json
    sessionid = req.get("sessionId")
    timestamp = req.get("timestamp")
    result = req.get("result")
    rquery = result.get("resolvedQuery")
    
    # speech is simply a string and ".format" allows us to add the data that we want to sections with {}
    speech = "My session ID is {}. The time stamp is {}. Your input was {}. We will add this to a database".format(sessionid, timestamp, rquery)
    
    # this is a python dictionary with the speech string embedded in the speech and displyText varibiables  
    out= {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": "test-api-app"
    }

    print("Request:")
    print(json.dumps(req, indent=4))

    res = json.dumps(out, indent=4)
    print(res)
    
    # I think make_response converts the python to a json file with a header that can be interpreted on the other end  
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
