from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from argparse import ArgumentParser
import time

from flask_ngrok import run_with_ngrok
import os
from os import environ
import sys
import result

app = Flask(__name__)
run_with_ngrok(app)

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN',None)
channel_secret = os.getenv('LINE_CHANNEL_SECRET',None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/")
def home():
    return "<h1>Hello, this is Anto's line bot from windows</h1>"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
      handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
      
    return 'OK'


world_case = result.Scrapetest()
with world_case as wc:
  world_result = wc.get_world_cases()
  thailand_result = wc.get_thailand_cases()
  usa_result = wc.get_usa_cases()

clock = time.ctime()
split_clock = clock.split(' ')
time_info = [t for t in split_clock if ':' in t]
current_time = time_info[0]

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  msg_from_usr = event.message.text
  msg_from_usr = msg_from_usr.strip().lower()
  if msg_from_usr == 'covid':
    line_bot_api.reply_message(
      event.reply_token,
      [
      TextSendMessage(text=world_result),
      TextSendMessage(text=thailand_result),
      TextSendMessage(text=usa_result),
      TextSendMessage(text="Stay Safe!")
      ]
      )
  elif msg_from_usr == 'hi':
    line_bot_api.reply_message(
        event.reply_token,
        [
        TextSendMessage(text="'sup"),
        TextSendMessage(text="How are you?")
        ]
        )


if __name__ == "__main__":
  app.run()
