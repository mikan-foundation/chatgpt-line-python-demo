# demo02 CLI上で対話形式でGPT-3.5 turboと会話できるデモ

import os
from os.path import join, dirname
from dotenv import load_dotenv
import openai

#Dotenvを初期化
load_dotenv(verbose=True)

#.envファイルのパスを指定：main.pyの場所＋.envファイル
dotenv_path= join(dirname(__file__), ".env")
# .envファイルを読み込み
load_dotenv(dotenv_path=dotenv_path)

#環境変数としてAPI KEYを読み込み
API_KEY = os.environ.get("GPT_API_KEY")

openai.api_key = API_KEY

#事前プロンプト：初期化項目
initial_prompt = [
    {"role": "system", "content": "5歳くらいの人でもわかるように回答してください"},
    {"role": "system", "content": "100文字以内で回答してください"}
]

messages = initial_prompt

#メインループ
while(True) :
  # ユーザーからの入力を受け付ける
  print("----------------")
  print("ボット：質問してください")
  print("----------------")
  prompt = str(input())

  # 「終了」とCLIで入力されたら自動で終了します
  if(prompt == "終了"): exit()

  # 「リセット」と入力されたら、事前プロンプトをリセットします
  if(prompt == "リセット"):
    messages = initial_prompt

  # 過去のメッセージとユーザーからの入力を結合
  messages.append( {"role":"user", "content": prompt})

  # APIに過去のmessagesのやりとりを送ります
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=messages
  )

  # assistantがroleのMessageオブジェクトが結合されます
  messages.append(response.choices[0]["message"]) 
  print("ChatGPTの回答：")
  # APIからのレスポンスを表示
  print(response.choices[0]["message"]["content"].strip())
  print("----------------")
  
