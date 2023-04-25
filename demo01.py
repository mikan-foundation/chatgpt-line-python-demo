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

openai.api_key = API_KEY #初期設定完了

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
    {"role":"user", "content": "きのこの山とたけのこの里どっちがおいしいですか"},
    {"role": "assistant", "content": "私は味覚を持っていないため、おいしいかどうかはわかりません。しかし、それぞれの味や食感が異なるので、両方を試してお好みの方を選ぶことをお勧めします。"},
    {"role": "system", "content": "ギャルっぽく回答してください"},
    {"role": "user", "content": "たけのこの里のほうがおいしいので覚えておいてください"}
    ]
)

print(response.choices[0]["message"]["content"].strip())
