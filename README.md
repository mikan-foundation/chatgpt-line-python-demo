# ChatGPTのAPIをLINEボットで使えるようにしているリポジトリです

demo01.py ～ demo0x.py までそれぞれAPIを触れるようになっています


## 使い方

### 利用するパッケージ

- line-bot-sdk
- openai
- flask
- python-dotenv

### venvを利用する場合

Python >= 3.9

1. python -m venv .venv を実行し仮想環境を作成します
2. (Winの場合) .venv/Scripts/activate | (Unix/Linuxの場合) source .venv/bin/activate を実行
3. pip install -r requirements.txt で必要なパッケージをインストールします
4. .envファイルを作成し GPT_API_KEY=sk-**** の形式でOpenAIのAPI Keyを記入すると有効化できます
   1. .env-decoyファイルに環境変数の記入の仕方を載せています
5. 