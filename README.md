# 前提

任意の python 環境があるものとします

# インストール

```cmd
git clone https://github.com/seichi042I/transcribe_tool
cd transcribe_tool
pip install -r requirements.txt
```

# 使い方

## 起動

```bash
python tstool.py <音声ファイルディレクトリ> [書き起こしファイル]
```

書き起こしファイルのパスを指定しなかった場合は、音声ファイルディレクトリの親ディレクトリに新しく作成されます。

## 操作方法

テキストエディタにフォーカスしないといけないので、適当なところをクリックしてください。

### 再生

- 現在の行の音声を再生：`Shift + Space`
- 次の音声を再生：`Shift + Enter`
- 前の音声を再生：`Ctrl + Shift + Enter`

### カーソル移動

- 上に移動：`Ctrl + I`
- 左に移動：`Ctrl + J`
- 下に移動：`Ctrl + K`
- 右に移動：`Ctrl + L`
- 上に 5 つ移動：`Shift + Ctrl + I`
- 左に 5 つ移動：`Shift + Ctrl + J`
- 下に 5 つ移動：`Shift + Ctrl + K`
- 右に 5 つ移動：`Shift + Ctrl + L`

### その他

- 元に戻す：`Ctrl + Z`
- やり直し：`Ctrl + Shift + Z`
- 変更を保存：`Ctrl + S`
- 行を削除：`Shift + BackSpace`
- 行の先頭・末尾にカーソルをトグル：`Tab`

# whisper による書き起こし

```bash
python whisper_transcribe.py <音声ファイルディレクトリ>
```

実行すると、音声ファイルがあるディレクトリの親ディレクトリに書き起こしファイルが生成されます。

# 補足

whisper 等で文字起こししたものをチェックするときに使用することを想定して作りました。
人力文字起こしツールとしては、不便かもしれません。
