#!/bin/sh

echo "Waiting for database..."
while ! pg_isready -h db -p 5432 -q; do
  sleep 1
  echo "Waiting for db to start..."
done
echo "Database is ready."
