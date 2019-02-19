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

app = Flask(__name__)i

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["wLNBgYDgXqPR0Lw+smPNBJ9ToSx4NQnJgbJuCt7UYvl3tItaT2zELErsn/vXExcuV6YNbi6Ni0hxjzlwQtTk5XlT3CqaYd2eFOs2DbOHPWsFVQx+WmZD2phYS3dUusRob8IH+UpDFQk0pl0JDh30cwdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["7d10760d5064ebdd0bceb9b15782aef2"]

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

