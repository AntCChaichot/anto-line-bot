#!/usr/bin/bash

export LINE_CHANNEL_SECRET="YOUR_LINE_CHANNEL_SECRET"
export LINE_CHANNEL_ACCESS_TOKEN="YOUR_LINE_CHANNEL_ACCESS_TOKEN"
export USE_NGROK=True
export FLASK_ENV=development
export FLASK_APP=app.py
flask run
