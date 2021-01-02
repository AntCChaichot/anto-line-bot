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

from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
line_bot_api = LineBotApi('eINJlmnTm6Rowb6MAXseQzmKSniHBwYBn0dLZduj7d452Zt5RzkteCRxcbbTnfdXkfqeSAHZT/m0aaG7QOhK2VDaLG8PgxaqutcMXlHoTu13vX086cTZL7r9a/faiteAp95OP1wSj0U3LB/QCDs3YAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7ea429370d4067dedc898531df9c3f1f')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


#if __name__ == "__main__":
app.run()
