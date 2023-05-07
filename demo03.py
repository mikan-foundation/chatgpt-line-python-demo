from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from dotenv import load_dotenv

from os import environ
from os.path import dirname, join

# Dotenvを初期化
load_dotenv(verbose=True)

# .envファイルのパスを指定：main.pyの場所＋.envファイル
dotenv_path = join(dirname(__file__), ".env")
# .envファイルを読み込み
load_dotenv(dotenv_path=dotenv_path)

LINE_CHANNEL_ACCESS_TOKEN = environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = environ.get("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)


@app.route('/callback', methods=['POST'])
def callback():
    # ヘッダー情報から X-Line-Signature の署名情報を取得
    signature = request.headers['X-Line-Signature']
    
    # リクエストをテキストで取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名を検証して、問題なければhandleに定義されている関数を実行
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# メッセージが送られてきたら、handlerに定義されている関数を実行
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 送られてきたメッセージをそのまま返します
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(port=4000)
