#TO DO: THIS IS A ZENDUTY SERVICE THAT RAISES ALERTS ON BEHALF OF OTHER SERVICES THAT RESULT IN UNIQUE INCIDENTS PER QUERY :
# i) Start Flask app   ii) Redis server running in background    iii) Services send payloads as : #curl -- url, header, data.. directed to the route   iv) Add rq worker to process Redis queue to post alerts

# Services, admin (user)

import os, subprocess

from flask import Flask, request
import requests
import logging
import json

from redis_config import redis_conn
from rq import Queue

import uuid

from message import Alert


# Initialize Flask app (HTML rendering)
app = Flask(__name__)

# Setup basic logging
logging.basicConfig(level=logging.INFO)


q = Queue(connection=redis_conn)

redis_conn.set("tags", json.dumps([]))
redis_conn.set("entity_ids", json.dumps([]))



@app.route("/")  # Requests to root URL 
def home():
    return "Zenduty_Dashboard"
 

#Verify payload, check entity ids, 
@app.route("/raise_alert", methods = ["POST"])    #Services
def raise_alert():
    payload = request.get_json()
    message, summary, alert_type = payload['message'], payload['summary'], payload['alert_type']
    alert = Alert(message, summary, alert_type)

    tag = None
    if('tag' in payload['payload']):
        tag = payload['payload']['tag']
    
    q.enqueue(alert.post_alert, tag)

    # logging.info(tags)
    return "Your alert was raised"


#entity ids being assigned in flask or in redis

#Multiple queues or single

#num_workers


@app.route("/resolve_incident", methods=['POST'])     #Admin
def resolve_incident():
    
    #os.system("kill -TERM $(pgrep -f rq)") #complete current task, stop worker, queue new tasks but don't process

    payload = request.get_json()
    message, summary, alert_type, entity_id = payload['message'], payload['summary'], payload['alert_type'], payload['entity_id']

    alert = Alert(message, summary, alert_type)
    alert.set_entity_id(entity_id)
    
    q.enqueue(alert.resolve_alert, entity_id)


    #subprocess.Popen(["rq", "worker"])

    return "Incident resolved" 





if __name__ == '__main__':    
    app.run()


#Port, updates, deprecated call, redis-server, sleep 



#Zenduty entity id incident generation