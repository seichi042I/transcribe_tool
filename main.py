import os
import sys
from typing import Callable,Dict
from pathlib import Path
import platform
import customtkinter as ctk
from tkinter import font
import tkinter as tk
from tkinter import ttk

from audio_manager import AudioManager

ctk.set_appearance_mode("dark")

# 現在のファイルの絶対パスを取得
current_file_path = os.path.abspath(__file__)

# ディレクトリのパスを取得
tmpdir = os.path.dirname(current_file_path)

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
        with open(file_path.replace('.txt','_edit.txt'), 'w', encoding='utf-8') as file:
            file.write(text_widget.get('1.0', ctk.END))
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
        
# アプリケーションの作成
def create_app(directory,text_file):
    root = ctk.CTk()  # CustomTkinterのルートウィンドウを作成
    root.geometry("800x600")
    root.title("ts tool")

    # PanedWindowを使用してリストボックスとテキストエディタを配置
    pwindow = ttk.Panedwindow(root, orient='horizontal')
    pwindow.pack(fill='both', expand=True)


    # テキストエディタの作成
    os_font = get_os_specific_font()
    text_editor = ctk.CTkTextbox(pwindow, font=os_font, wrap="none",undo=True)  # CustomTkinterのテキストウィジェット
    bg_color = text_editor._fg_color[1]
    fg_color = text_editor._fg_color[0]
    
    # リストボックスの作成
    audio_manager = AudioManager(pwindow, Path(directory), {"font": os_font,"bg":bg_color,"fg":fg_color})
    audio_manager.listbox.bind("<Double-1>", lambda e: audio_manager.on_select_item())
    
    # ショートカット
    def cursor_step(callback):
        index = text_editor.index("insert")
        line = int(index.split(".")[0])
        position = int(index.split(".")[1])
        callback({"current_cursor_position":int(text_editor.index('insert').split(".")[0])-1})
        text_editor.mark_set('insert',f'{audio_manager.current_index+1}.{position}')
        text_editor.see("insert")
        
        return 'break'
    
    text_editor.bind('<Control-Shift-Return>', lambda e: cursor_step(audio_manager.play_previous))
    text_editor.bind('<Shift-space>', lambda e: cursor_step(audio_manager.play_current))
    text_editor.bind('<Shift-Return>', lambda e: cursor_step(audio_manager.play_next))
    
    # カーソル移動
    def mv_cursor(direction:str):
        index = text_editor.index("insert")
        line = int(index.split(".")[0])
        position = int(index.split(".")[1])
        if direction == "up":
            audio_manager.back()
            text_editor.mark_set('insert',f'{line-1}.{position}')
        elif direction == "down":
            audio_manager.next()
            text_editor.mark_set('insert',f'{line+1}.{position}')
        elif direction == "right":
            text_editor.mark_set('insert','insert + 1c')
        elif direction == "left":
            text_editor.mark_set('insert','insert - 1c')
        else:
            return 'break'
        text_editor.see("insert")
        return 'break'
        
    text_editor.bind('<Control-i>', lambda e: mv_cursor('up'))
    text_editor.bind('<Control-k>', lambda e: mv_cursor('down'))
    text_editor.bind('<Control-l>', lambda e: mv_cursor('right'))
    text_editor.bind('<Control-j>', lambda e: mv_cursor('left'))
    
    # Undo Redo
    # text_editor.bind('<Control-z>', lambda e: text_editor.edit_undo())
    text_editor.bind('<Control-Shift-Z>', lambda e: text_editor.edit_redo())
    
    pwindow.add(audio_manager.listbox)
    pwindow.add(text_editor)
    
    
    # テキストファイルの読み込み
    if text_file:
        load_text_file(text_file, text_editor)
        
    # 保存ボタンの作成
    save_button = ctk.CTkButton(root, text="Save", command=lambda: save_text(text_file, text_editor))
    save_button.pack(fill='x')
    
    def on_key_press(e):
        global text_edhitor, text_file
        
        if e.keysym == 's' and e.state & 0x0004:  # Ctrl + S
            save_text(text_file, text_editor)
            return "break"
        
    root.bind('<Control-s>', on_key_press)
    root.bind('<Control-S>', on_key_press)  # 大文字Sにも対応
    return root


# メイン
if __name__ == "__main__":
    global current_index
    current_index = 0
    directory = sys.argv[1]  # 音声ファイルが格納されたディレクトリを指定
    text_file = sys.argv[2]
    app = create_app(directory,text_file)
    app.mainloop()
