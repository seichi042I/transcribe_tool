import os
import customtkinter as ctk
import platform



# テキストファイルを読み込む関数
def load_text_file(file_path, text_widget):
    # ファイルが存在するかチェック
    if not os.path.exists(file_path):
        # ファイルが存在しない場合、新規作成
        open(file_path, 'w', encoding='utf-8').close()

    try:
        with open(file_path, 'r+', encoding='utf-8') as file:  # 読み書きモードで開く
            text_widget.delete('1.0', ctk.END)  # 既存のテキストをクリア
            text_widget.insert('1.0', file.read())  # ファイル内容を挿入
    except UnicodeDecodeError:
        print(f"ファイル {file_path} の読み込み中にエラーが発生しました。")


# テキスト内容をファイルに上書き保存する関数
def save_text(file_path, text_widget):
    try:
        with open(str(file_path), 'w', encoding='utf-8') as file:
            file.write(text_widget.get('1.0', 'end'))
        print("ファイルが保存されました")
    except Exception as e:
        print(f"保存中にエラーが発生しました: {e}")

# OSに基づいてフォントを選択する関数
def get_os_specific_font():
    system_name = platform.system()
    if system_name == 'Windows':
        return ctk.CTkFont(family="メイリオ", size=16,weight='bold')  # Windows用フォント
    elif system_name == 'Darwin':  # macOSの場合
        return ctk.CTkFont(family="Monaco", size=16,weight='bold')  # macOS用フォント
    else:  # Linuxやその他のOS
        return ctk.CTkFont(family="Monospace", size=16,weight='bold')  # Ubuntu用フォント
 