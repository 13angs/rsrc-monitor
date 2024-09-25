#!/bin/bash

# docker-compose -f /home/bangz/apps/rsrc-monitor/config/docker-compose.prod.yaml up fuel

# Get the container ip
export CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' config-rsrc-monitor-1)
echo "Container IP is $CONTAINER_IP."
echo

echo "Scraping the fuel data..."
response=$(curl http://$CONTAINER_IP:8000/api/scrape/fuel)
echo

status=$(echo "$response" | jq '.status')
echo "Status is $status"