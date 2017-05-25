#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    sessionid = req.get("sessionId")
    timestamp = req.get("timestamp")
    result = req.get("result")
    rquery = result.get("resolvedQuery")
    
    speech = "My session ID is {}. The time stamp is {}. Your input was {}. We will add this to a database".format(sessionid, timestamp, rquery)
    
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
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
