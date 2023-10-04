#!/bin/sh

while ! nc -z server 8000;
    do sleep 3;
done
echo "Server started"

exec "$@"
