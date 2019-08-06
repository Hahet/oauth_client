import json

import requests
from flask import Flask, request, Request, render_template, \
    jsonify, redirect
from config import config


app = Flask(__name__)


def log(*arg, **kwargs):
    print(*arg, **kwargs)


@app.route('/')
def index():
    return render_template('index.html', config=config)


@app.route('/oauth/redirect')
def oauth_redirect():
    # 获取到id
    log('aaa')
    authorization_code = request.args.get('code')
    log('authorization code:', authorization_code)
    # 跨域请求, 使用client和client_secret换取token
    # 0 使用token_uri client_id client_secret authorization_code拼接url
    # 使用
    # {token_uri}?client_id = {client_id} & client_secret = {client_secret} & code = {authorization_code}
    url = '{token_uri}?client_id={client_id}&client_secret={client_secret}&code={authorization_code}'.format(authorization_code=authorization_code,
                                                                                                             **config)
    log('rul', url)
    r = requests.post(
        url=url,
        headers={"accept": 'application/json'}
    )
    # 1 返回的数据解析成json格式, 获取其中的 access_token
    access_token = r.json()['access_token']
    log("access token: ", access_token)
    # 使用token换取数据, githubde o
    # 2 补全headers中的 Authorization
    Authorization = 'token {access_token}'.format(access_token=access_token)
    r = requests.get(
        url=config['api_uri'],
        headers={
            "accept": 'application/json',
            "Authorization": Authorization,
        }
    )
    # 返回的数据解析成json格式
    u = r.json()
    error_log = str(u) + '\n' + str(config)
    # 测试返回数据的login name
    assert u['name'] == config['login'], error_log
    return render_template('redirect.html', github=u)


if __name__ == "__main__":
    # Don't use debug=True, because it disables VS CODE debugger
    cfg = dict(
        # debug=True,
        port=8080
    )
    app.run(**cfg)
