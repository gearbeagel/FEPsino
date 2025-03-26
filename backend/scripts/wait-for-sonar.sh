#!/bin/sh

echo "Waiting for SonarQube..."
while ! curl -s "$SONAR_HOST_URL/api/system/status" | grep -q "UP"; do
  sleep 1
  echo "Waiting for SonarQube to start..."
done
echo "SonarQube is ready."