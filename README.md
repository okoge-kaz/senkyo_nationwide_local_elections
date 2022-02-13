# 株式会社センキョ 統一地方選挙　スクレイピングリポジトリ

## 仮想環境の整備

1. 仮想環境作成 : `python3 -m venv .venv` 
2. 仮想環境に入る : `source .venv/bin/activate`
3. 依存環境の整備 : `python3 -m pip install -r requirements.txt`
4. 仮想環境から抜ける : `deactivate`

- `requirements.txt`を作成する
`python3 -m pip freeze > requirements.txt`

- 仮想環境内にパッケージをインストール
`python3 -m pip install requests`
`python3 -m ppip install selenium`

参考記事 : [URL](https://maku77.github.io/python/env/venv.html)
パッケージ関連 : [URL](https://rinoguchi.net/2020/08/python-scraping-library.html)


