#!/bin/bash

# Get the container ip
export CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' config-rsrc-monitor-1)
echo "Container IP is $CONTAINER_IP."
echo

echo "Scraping the fuel data..."
response=$(curl http://$CONTAINER_IP:8000/api/scrape/fuel)

message=$(echo "$response" | jq '.message')
status=$(echo "$response" | jq '.status')

echo $message
echo

if [ "$status" -eq 404 ]; then
    echo "Now alerting to telegram..."
    response=$(curl http://$CONTAINER_IP:8000/api/alert/fuel)
    
    message=$(echo "$response" | jq '.message')
    echo $message
fi
