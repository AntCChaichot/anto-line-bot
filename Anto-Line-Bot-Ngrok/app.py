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

import time
import requests, json

import os
from os import environ
import sys

from typing import Dict, Tuple

import result # for covid
from weather import weatherResult # for weather

# run with "source start_flask.sh"
def create_app():
  app = Flask(__name__)

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

  # Initialize our ngrok settings into Flask
  app.config.from_mapping(
      BASE_URL="http://localhost:5000",
      USE_NGROK=os.environ.get("USE_NGROK", "False") == "True" and os.environ.get("WERKZEUG_RUN_MAIN") != "true")

  

  if app.config.get("ENV") == "development" and app.config["USE_NGROK"]:
  # pyngrok will only be installed, and should only ever be initialized, in a dev environment
    from pyngrok import ngrok, conf

  # Get the dev server port (defaults to 5000 for Flask, can be overridden with `--port`
  # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 5000
  
    def log_event_callback(log):
      print(str(log))

    conf.get_default().log_event_callback = log_event_callback
    conf.get_default().region = "jp"

  # Set Line Webhook URL
    def setWebhook(endpoint, CHANNEL_ACCESS_TOKEN):
      endpointFixed = "https://" + endpoint.split('//')[-1] + '/callback'
      url = "https://api.line.me/v2/bot/channel/webhook/endpoint"
      header = {'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN}
      body = json.dumps({'endpoint': endpointFixed})
      response = requests.put(url=url, data=body, headers=header)
      print(response)
      obj = json.loads(response.text)
      print(obj)

  # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))
    print("Setting webhook")
    setWebhook(public_url, channel_access_token)

  # Update any base URLs or webhooks to use the public ngrok URL
    app.config["BASE_URL"] = public_url
    init_webhooks(public_url)
    
    
  
  # ... Initialize Blueprints and the rest of our app


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
    LINE_DESTINATION_ID = "U831b6e5d5cdb92a590017c20bb007ab8"
    global userId
    try:
      userId, text, reply_token, destination = process_body(body)
      assert LINE_DESTINATION_ID == destination
      profile = line_bot_api.get_profile(userId)
      print('-'*70)
      print(f"User ID: {userId} \nText: {text} \nReply Token: {reply_token} \nName: {profile.display_name}")
      print('-'*70)
    except ValueError: #not enough items when returned (only dest)
      destination = process_body(body)
      assert LINE_DESTINATION_ID == destination
      print("Webhook Verification successful")
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
    try:
      event_type = body_data[0]['type']
      token = body_data[0]['replyToken']
      userid = body_data[0]['source']['userId']
      message = body_data[0]['message']
      if message['type'] == 'text': #process message type response
        message_text = message['text']
      else:
        return
    except UnboundLocalError:
      return
    except IndexError: # for verifying (no items in events)
      return dest
    return (userid, message_text, token, dest)

  def call_covid_data() -> Tuple[str]:
    world_case = result.Scrapetest()
    with world_case as wc:
      world= wc.get_world_cases()
      thailand= wc.get_thailand_cases()
      usa= wc.get_usa_cases()
    return (world, thailand, usa)


  def call_weather_all_data(zipcode: str, input_country: str = 'th') -> Dict[str, list]:
    all_weather = weatherResult(zipcode, input_country)
    all_data = all_weather.get_all_data()
    return all_data

  def thai_zipcode_list():
    with open("thai_zipcodes.json", "r") as zc_file:
      zc = [e.strip().split("\"")[3] for e in zc_file if "zip" in e]
    return zc


  @handler.add(MessageEvent, message=TextMessage)
  def handle_message(event):
    msg_from_usr = event.message.text
    msg_from_usr = msg_from_usr.strip().lower()
    if msg_from_usr == 'covid' or msg_from_usr == 'โควิด':
      line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Getting Data, Hang in there!"))
      world_result, thailand_result, usa_result = call_covid_data()
      line_bot_api.push_message(
        userId,
        [
        TextSendMessage(text=world_result),
        TextSendMessage(text=thailand_result),
        TextSendMessage(text=usa_result),
        TextSendMessage(text="Stay Safe!")
        ]
        )
    elif msg_from_usr == 'hi' or msg_from_usr == 'สวัสดี':
      line_bot_api.reply_message(
        event.reply_token,
        [
        TextSendMessage(text="'sup"),
        TextSendMessage(text="How are you?")
        ]
        )
      #elif msg_from_usr in thai_zipcode_list():
    else:
      try:
        zc, coun = msg_from_usr.split(" ")
        weather_data = call_weather_all_data(zc, coun)
      except ValueError: #only zipcode is passed in
        weather_data = call_weather_all_data(msg_from_usr)
      try:
        line_bot_api.reply_message(
          event.reply_token,
          [
          TextSendMessage(text=f"Country: {weather_data['Country']} \nCity: {weather_data['City']}"),
          TextSendMessage(text=f"""Date: {weather_data['Weather'][0][0]} 
Temperature: {weather_data['Weather'][0][1]}
Feels Like: {weather_data['Weather'][0][2]}
Humidity: {weather_data['Weather'][0][3]}
Description: {weather_data['Weather'][0][4]}"""
          ),
          TextSendMessage(text=f"""Date: {weather_data['Weather'][1][0]} 
Temperature: {weather_data['Weather'][1][1]}
Feels Like: {weather_data['Weather'][1][2]}
Humidity: {weather_data['Weather'][1][3]}
Description: {weather_data['Weather'][1][4]}"""
          ),
          TextSendMessage(text=f"""Date: {weather_data['Weather'][2][0]} 
Temperature: {weather_data['Weather'][2][1]}
Feels Like: {weather_data['Weather'][2][2]}
Humidity: {weather_data['Weather'][2][3]}
Description: {weather_data['Weather'][2][4]}"""
          ),
          TextSendMessage(text=f"""Date: {weather_data['Weather'][3][0]} 
Temperature: {weather_data['Weather'][3][1]}
Feels Like: {weather_data['Weather'][3][2]}
Humidity: {weather_data['Weather'][3][3]}
Description: {weather_data['Weather'][3][4]}"""
          )
          ]
          )
      except TypeError: #returned none or message is something else
        line_bot_api.reply_message(
            event.reply_token,
            [
              TextSendMessage(text="Sorry, I do not understand the message because: \n  - Data may not be found in the system! \n  - It's not code-acceptable yet \nHave your message back :D"),
            TextSendMessage(text=event.message.text)
            ]
            )
      #else:
      #line_bot_api.reply_message(
      #    event.reply_token,
      #   TextSendMessage(text=event.message.text)
      #    )

  return app

