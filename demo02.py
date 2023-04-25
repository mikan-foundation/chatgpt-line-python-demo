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
messages = [
    {"role": "system", "content": "5歳くらいの人でもわかるように回答してください"},
    {"role": "system", "content": "100文字以内で回答してください"}
]

while(True) :
  print("----------------")
  print("ボット：質問してください")
  print("----------------")
  prompt = str(input())

  if(prompt == "終了"): exit()

  messages.append( {"role":"user", "content": prompt})

  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=messages
  )

  messages.append(response.choices[0]["message"]) #assistantがroleのMessageオブジェクトがappend（されるはず）
  print("ChatGPTの回答：")
  print(response.choices[0]["message"]["content"].strip())
  print("----------------")
  
