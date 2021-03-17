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

import os
from os import environ
import result

import requests, json
from typing import Dict

app = Flask(__name__)

line_bot_api = LineBotApi(environ['MY_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(environ['MY_CHANNEL_SECRET'])


@app.route("/")
def home():
    return "<h1>Hello, this is Anto's line bot!</h1>"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print("# Webhook event:\n","-"*100,body)
    print("-"*100)
    LINE_DESTINATION_ID = "U831b6e5d5cdb92a590017c20bb007ab8"
    try:
      userId, text, reply_token, destination = process_body(body)
      assert LINE_DESTINATION_ID == destination
      print(f"User ID: {userId} \nText: {text} \n Reply Token: {reply_token}")
      print("-"*100)
    except ValueError: #not enough items when returned to unpack (only dest)
      destination = process_body(body)
      assert LINE_DESTINATION_ID == destination
      print("Webhook Verification is successful")
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


def process_body(original_body: str):
  body = json.loads(original_body)
  body_data = [e for e in body['events']]
  dest = body['destination']
  event_type = body_data[0]['type']
  try:
    token = body_data[0]['replyToken']
    userid = body_data[0]['source']['userId']
    message = body_data[0]['message']
    if message['type'] == 'text':
      message_text = message['text']
    else:
      return
  except UnboundLocalError:
    return
  except IndexError: # for verifying (no items in events)
    return dest
  return (userid, message_text, token, dest)


def call_data():
  world_case = result.Scrapetest()
  with world_case as wc:
    world= wc.get_world_cases()
    thailand= wc.get_thailand_cases()
    usa= wc.get_usa_cases()
  return (world, thailand, usa)




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  msg_from_usr = event.message.text
  msg_from_usr = msg_from_usr.strip().lower()
  if msg_from_usr == "covid":
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Getting Data, Please wait"))
    world_result, thailand_result, usa_result = call_data()
    line_bot_api.push_message(
        userId,
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
        TextSendMessage(text="'sup")
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host = '0.0.0.0', port=port)
