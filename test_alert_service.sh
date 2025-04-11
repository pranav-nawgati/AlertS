#!/bin/bash

# Start the Redis server
redis-server &

# Run the Flask application
python3 alert_service.py &

# Wait for the Flask app to start
sleep 5

# Resolve an incident

rq worker &

curl --location http://127.0.0.1:5000/raise_alert --header 'Content-Type: application/json' --data '{
"message": "dispenser 10 is not pulling data for more than 5 minutes at mglsion(1418)",
"summary": "",
"alert_type": "critical",
"payload": {
"tag": "dispenser 10 is not pulling data"
}
}'


curl --location http://127.0.0.1:5000/raise_alert --header 'Content-Type: application/json' --data '{
"message": "Stream License Expired at 1502(iglshantipath)",
"summary": "",
"alert_type": "critical",
"payload": {
"tag": "stream_license_expired_1502"
}
}'


curl --location http://127.0.0.1:5000/raise_alert --header 'Content-Type: application/json' --data '{
"message": "dispenser 10 is not pulling data for more than 5 minutes at mglsion(1418)",
"summary": "",
"alert_type": "critical",
"payload": {
"tag": "dispenser 10 is not pulling data"
}
}'

curl --location http://127.0.0.1:5000/resolve_incident --header 'Content-Type: application/json' --data '{
"message": "Stream License Expired at 1502(iglshantipath)",
"summary": "",
"alert_type": "resolved",
"entity_id": "3ff0da20-91f3-4fc0-a943-234743f2"
}'



# Start the RQ worker
