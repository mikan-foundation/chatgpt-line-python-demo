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

while(True) :
  print("質問してください")
  prompt = str(input())

  if(prompt == "終了"): exit()

  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
    {"role":"user", "content": prompt}
    ]
  )

  print(response.choices[0]["message"]["content"].strip())
