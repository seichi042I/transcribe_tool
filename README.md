# 前提
任意のpython環境があるものとします

# インストール
```cmd
git clone https://github.com/seichi042I/transcribe_tool
cd transcribe_tool
pip install -r requirements.txt
```
# 使い方
## 起動
```bash
python main.py <音声ファイルがあるディレクトリパス> <書き起こしファイルのパス>
```

## 操作方法
最初に、テキストエディタにフォーカスしないといけないので、適当なところをクリックしてください。
### 再生
- 選択中の音声を再生：`Shift + Space`
- 次の音声を再生：`Shift + Enter`
- 前の音声を再生：`Ctrl + Shift + Enter`

### カーソル移動
- 上に移動：`Ctrl + I`
- 左に移動：`Ctrl + J`
- 下に移動：`Ctrl + K`
- 右に移動：`Ctrl + L`

### その他
- 元に戻す：`Ctrl + Z`
- やり直し：`Ctrl + Shift + Z`
- 変更を保存：`Ctrl + S`
- 行を削除：（未実装）

# 補足
whisper等で文字起こししたものをチェックするときに使用することを想定して作りました。
人力文字お越しツールとしては、不便かもしれません。
