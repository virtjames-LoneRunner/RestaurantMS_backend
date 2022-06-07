#! /bin/bash

SERVICE="uvicorn"
if pgrep -x "$SERVICE" > /dev/null
then
    echo "$SERVICE is running"
else
    echo "$SERVICE stopped"
    cd /home/james_main/api-hnjplus.jamesvirtudazo.com/main
    /home/james_main/hnjplusenv/bin/uvicorn main.asgi:application --reload --host 0.0.0.0 --port 8080 --ssl-keyfile=key.pem --ssl-certfile=crt.pem
fi
