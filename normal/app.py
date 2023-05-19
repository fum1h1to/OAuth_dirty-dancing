from flask import Flask, render_template, request, session, redirect
import random, string
from urllib.parse import urlencode
from dotenv import load_dotenv
import os
from datetime import timedelta 
import requests
from requests.auth import HTTPBasicAuth

# load envファイル
load_dotenv()

app = Flask(__name__)

app.secret_key = 'normal'
app.permanent_session_lifetime = timedelta(minutes=1)

# stateの長さ
STATE_LEN = 30

# redirect_uri
REDIRECT_URI = 'http://localhost:8080/callback'

# OAuthに必要なClient IDとClient Secret
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def randomname(n):
  '''
  ランダムな文字列を生成する
  '''
  randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
  return ''.join(randlst)

@app.route('/')
def index():
  '''
  トップページ（正常）
  '''
  return render_template('index.html')

@app.route('/oauth')
def oauth():
  '''
  OAuthの認証を行う
  '''

  session.permanent = True 
  state = randomname(STATE_LEN)
  session['state'] = state
  print(session)

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

@app.route('/callback')
def callback():
  '''
  OAuthのコールバックを受け取る
  '''
  if 'state' not in session:
    return render_template('error.html', message="stateがありません"), 400
  
  if request.args.get('state') != session['state']:
  # if True:
    return render_template('error.html', message='stateが一致しません'), 400

  code = request.args.get('code')
  if not code:
    return render_template('error.html', message='codeがありません'), 400
  print(code)

  base_url = "https://accounts.google.com/o/oauth2/token"
  params = {
    "code": code,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code"
  }
  headers = {
    "Content-Type": "application/x-www-form-urlencoded"
  }
  response = requests.post(base_url, headers=headers, data=params, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
  if response.status_code != 200:
    return render_template('error.html', message='access tokenの取得に失敗しました'), 400

  token = response.json()['access_token']
  session['token'] = token

  return redirect('/profile'), 302

@app.route('/profile')
def profile():
  '''
  プロフィールを表示する
  ログインページのようなもの
  '''
  if 'token' not in session:
    return redirect('/'), 302

  base_url = "https://www.googleapis.com/oauth2/v1/userinfo"
  headers = {
    "Authorization": "Bearer " + session['token']
  }
  response = requests.get(base_url, headers=headers)
  if response.status_code != 200:
    return 'profileの取得に失敗しました', 400

  profile = response.json()
  return render_template('profile.html', profile=profile)

@app.route('/logout')
def logout():
  '''
  ログアウトする
  '''
  session.pop('token', None)
  return redirect('/'), 302

if __name__ == "__main__":
  app.run(port=8080, debug=True, host="localhost")