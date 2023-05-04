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

app.secret_key = 'evil'
app.permanent_session_lifetime = timedelta(minutes=1)

STATE_LEN = 30
CODE_VERIFIER_LEN = 64
REDIRECT_URI = 'http://localhost:8080/callback'
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def randomname(n):
  randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
  return ''.join(randlst)

@app.route('/')
def index():
  return render_template('evil.html')

@app.route('/oauth')
def oauth():
  session.permanent = True
  state = "l3H9t0clF7cbKNu4lVkcu1aUYpOEZG"

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


if __name__ == "__main__":
  app.run(port=9262, debug=True)