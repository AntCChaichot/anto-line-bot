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
import requests

line_bot_api = LineBotApi(environ['MY_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(environ['MY_CHANNEL_SECRET'])

app = Flask(__name__)
@app.route("/")
def home():
	return "<h1>Hello from anto-line-bot</h1>"

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

@app.route("/check")
def check():
	ret = requests.get('http://api.openweathermap.org/data/2.5/forecast?zip=10330,th&APPID=7743f38ce634083abe786e2d679955e3&units=metric')
	d = dict(ret.json())
	weather = dict()
	for data in d['list'][0:6]:
		weather = {'Date':data['dt_txt'], 'Temperature':data['main']['feels_like'], 'Humidity':data['main']['humidity'],'Description':data['weather'][0]['description']}
	return weather

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	msg_from_usr = event.message.text
	msg_from_usr = msg_from_usr.strip().lower()
	ret = requests.get('http://api.openweathermap.org/data/2.5/forecast?zip='+msg_from_usr+',th&APPID=7743f38ce634083abe786e2d679955e3&units=metric')
	d = dict(ret.json())
	current_weather = dict()
	info = []
	info.append(d['city']['country'])
	info.append(d['city']['name'])
	for data in d['list'][0:5]:
		temp = []
		temp.append(data['dt_txt'])
		temp.append(data['main']['feels_like'])
		temp.append(data['main']['humidity'])
		temp.append(data['weather'][0]['description'])
		info.append(temp)
	weather = {'Country':info[0], 'Name':info[1],'2':info[2],'3':info[3],'4':info[4],'5':info[5],'6':info[6]}
	try:
		line_bot_api.reply_message(event.reply_token,
		[
		TextSendMessage(text="Country: " + str(weather['Country']) + "\nName: " + str(weather['Name'])),
		TextSendMessage(text="Date/Time: " + str(weather['2'][0]) + "\nTemperature: " + str(weather['2'][1]) + "\nHumidity: " + str(weather['2'][2]) + "\nDescription: " + str(weather['2'][3])),		TextSendMessage(text="Date/Time: " + str(weather['3'][0]) + "\nTemperature: " + str(weather['3'][1]) + "\nHumidity: " + str(weather['3'][2]) + "\nDescription: " + str(weather['3'][3])),		TextSendMessage(text="Date/Time: " + str(weather['4'][0]) + "\nTemperature: " + str(weather['4'][1]) + "\nHumidity: " + str(weather['4'][2]) + "\nDescription: " + str(weather['4'][3])),		TextSendMessage(text="Date/Time: " + str(weather['5'][0]) + "\nTemperature: " + str(weather['5'][1]) + "\nHumidity: " + str(weather['5'][2]) + "\nDescription: " + str(weather['5'][3]))])
	except LineBotApiError as e:
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Out of Order"))

if __name__ == "__main__":
	port = int(os.environ.get("PORT",5000))
	app.run(host='0.0.0.0',port=port)
