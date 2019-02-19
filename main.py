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

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["ICkb9WxPciMbNUs3aX3CM3SOuI81me2EL2aWZbMmHRMzOv1hCtmmHDodTdoY9ioUtR3ZAce/1MAkGSI0NGS9N2+s89DdMsLyk7RKpE5Ur49yir5FMvWlOdZhT09gPMdqKUMxI2QHfcl1OyvA8PsDMwdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["5784d802f2b0ad193ee9fdd354197289"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

