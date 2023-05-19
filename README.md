# OAuth_dirty-dancing
このリポジトリは、dirty-dancingの検証用である。

# 使い方
## フォルダ構成
- `evil`

    偽サイトに関するフォルダ
- `normal`

    正規のサイトに関するフォルダ

## 起動の仕方
1. Pythonの仮想環境の構築
    ```
    python -m venv venv
    ```

2. 仮想環境の有効化

    開発環境がLinux, Macの場合
    ```
    source venv/bin/activate
    ```

    開発環境がWindowsの場合
    ```
    .\venv\Scripts\activate
    ```

    ※WindowsでGit Bashを使用している場合
    ```
    source venv/Scripts/activate
    ```

3. モジュールのインストール
    ```
    pip install -r requirements.txt
    ```

4. `.env`ファイルの準備
    ```
    cp .env.template .env
    ```

5. Oauthクライアントの作成

    今回はGoogleのOAuthクライアントを使用します。<br>
    [こちら](https://support.google.com/workspacemigrate/answer/9222992?hl=ja)を参考に作成してください。

    なお、認証済みのJavaScript生成元と認証済みのリダイレクトURIは以下の内容を追加してください。その他については任意で大丈夫です。

    認証済みのJavaScript生成元
    - `http://localhost:8080`

    認証済みのリダイレクトURI
    - `http://localhost:8080/callback`

6. 偽サイトと正規サイトの起動

    偽サイト
    ```
    cd evil
    python evil.py
    ```

    正規サイト
    ```
    cd normal
    python app.py
    ```

`http://localhost:9262`が偽サイト<br>
`http://localhost:8080`が正規サイトのURLとなる。