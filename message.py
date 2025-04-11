import requests

import time

import json

import uuid

from redis_config import redis_conn

integration_key = "2edbebb9-2e43-44d8-9e92-56b1bb8111f7"

account_id = "az6cq"


class Alert:
    
    def __init__(self, message, summary, alert_type = 'critical'):
        self.alert_message = message 
        self.alert_summary = summary 
        self.alert_type = alert_type
        self.entity_id = None

    def set_entity_id(self, entity_id):
        self.entity_id = entity_id


    def assign_entity_id(self, tag):
        tags = json.loads(redis_conn.get("tags"))
        entity_ids = json.loads(redis_conn.get("entity_ids"))
        
        if(tag in tags):
            entity_id = entity_ids[tags.index(tag)]
        else:
            entity_id = create_entity_id()
            tags.append(tag); entity_ids.append(entity_id)

            redis_conn.set("tags", json.dumps(tags))
            redis_conn.set("entity_ids", json.dumps(entity_ids))
        
        self.set_entity_id(entity_id)


    def remove_entity_id(self, entity_id):
        tags = json.loads(redis_conn.get("tags"))
        entity_ids = json.loads(redis_conn.get("entity_ids"))

        if(entity_id in entity_ids):
            idx = entity_ids.index(entity_id)
            entity_ids.remove(entity_id)
            tags.remove(tags[idx])
        
            redis_conn.set("tags", json.dumps(tags))
            redis_conn.set("entity_ids", json.dumps(entity_ids))


    def post(self):
        if(self.alert_type!='critical'):
            raise Exception("Alert type must be critical")
        payload = { "message": self.alert_message, "summary": self.alert_summary, "alert_type": self.alert_type}
        if(self.entity_id is not None):
            payload['entity_id'] = self.entity_id 
        
        #response = requests.post(url = f'https://www.zenduty.com/api/events/{integration_key}/', json = payload)
        response = requests.post(url = f"https://events.zenduty.com/integration/{account_id}/generic/{integration_key}/", json = payload)
        print(payload)
        print(response.status_code, response.text)
        time.sleep(100)
        
        


    def resolve(self):
        if(self.alert_type!='resolved'):
            raise Exception("Invalid alert type")
        payload = {"message": self.alert_message, "summary": self.alert_summary, "alert_type": self.alert_type, "entity_id": self.entity_id}
        
        #response = requests.post(url = f"https://www.zenduty.com/api/events/{integration_key}/", json = payload)    
        response = requests.post(url = f"https://events.zenduty.com/integration/{account_id}/generic/{integration_key}/", json = payload)
        print(payload)
        print(response.status_code, response.text)
        time.sleep(100)


    #functions to be queued

    def post_alert(self, tag):
        self.assign_entity_id(tag)
        self.post()


    def resolve_alert(self, entity_id):
        self.resolve()
        self.remove_entity_id(entity_id)



def create_entity_id():
    uuid_str = str(uuid.uuid4()).replace("-", "")
    return uuid_str