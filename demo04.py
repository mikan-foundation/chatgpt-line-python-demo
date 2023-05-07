from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from dotenv import load_dotenv

from os import environ
from os.path import dirname, join

import openai

# Dotenvを初期化
load_dotenv(verbose=True)

# .envファイルのパスを指定：main.pyの場所＋.envファイル
dotenv_path = join(dirname(__file__), ".env")
# .envファイルを読み込み
load_dotenv(dotenv_path=dotenv_path)

LINE_CHANNEL_ACCESS_TOKEN = environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = environ.get("LINE_CHANNEL_SECRET")
GPT_API_KEY = environ.get("GPT_API_KEY")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

openai.api_key = GPT_API_KEY

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
    # 送られてきたメッセージを変数に格納します
    msg = event.message.tex

    # ユーザーからのメッセージをAPIに送る形に整形します
    messages =  [{"role":"user", "content": msg}]

    # APIに過去のmessagesのやりとりを送ります
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", 
      messages=messages
    )
    # レスポンスをreply_message関数を使って送ります
    # TextSendMessageは、テキストを送るためのオブジェクトを作成する関数です
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response.choices[0]["message"]["content"].strip()))


if __name__ == "__main__":
    app.run(port=4000)
