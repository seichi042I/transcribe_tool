import os
import sys
from pathlib import Path
import customtkinter as ctk
import tkinter as tk

from audio_manager import AudioManager

from utils import load_text_file,save_text,get_os_specific_font

ctk.set_appearance_mode("dark")

# デリミタ設定
DELIMITER = ':'

# 現在のファイルの絶対パスを取得
current_file_path = os.path.abspath(__file__)

# ディレクトリのパスを取得
tmpdir = os.path.dirname(current_file_path)

# アプリケーションの作成
def create_app(wav_dirpath,text_file=None):
    root = ctk.CTk()  # CustomTkinterのルートウィンドウを作成
    root.geometry("800x600")
    root.title("ts tool")

    # テキストエディタの作成
    os_font = get_os_specific_font()
    text_widget = ctk.CTkTextbox(root, font=os_font, wrap="none",undo=True)  # CustomTkinterのテキストウィジェット
    bg_color = text_widget._fg_color[1]
    fg_color = text_widget._fg_color[0]
    
    # リストボックスの作成
    audio_manager = AudioManager(wav_dirpath, {"font": os_font,"bg":bg_color,"fg":fg_color})
    # audio_manager.listbox.bind("<Double-1>", lambda e: audio_manager.on_select_item())
    
    # テキストファイルの読み込み
    save_filepath = wav_dirpath.parent / "transcript_utf8_edit.txt"
    if text_file:
        load_text_file(text_file, text_widget)
    else:
        for path in audio_manager.wav_path_list:
            stem = path.stem
            text_widget.insert("end", f"{stem}:\n")
    
    # 再生ショートカット
    def play_step(text_widget,audio_manager,diff):
        index = text_widget.index("insert")
        line_idx = int(index.split(".")[0])
        position = int(index.split(".")[1])
        
        line = text_widget.get(f"{line_idx+diff}.0",f"{line_idx+diff}.end")
        stem = line.split(DELIMITER)[0]
        audio_manager.play(stem)
        text_widget.mark_set('insert',f'{line_idx+diff}.{position}')
        text_widget.see("insert")
        
        return 'break'
    
    text_widget.bind('<Control-Shift-Return>', lambda e: play_step(text_widget,audio_manager,-1))
    text_widget.bind('<Shift-space>', lambda e: play_step(text_widget,audio_manager,0))
    text_widget.bind('<Shift-Return>', lambda e: play_step(text_widget,audio_manager,1))
    
    # カーソル移動
    def mv_cursor(text_widget:ctk.CTkTextbox,direction:str):
        index = text_widget.index("insert")
        line = int(index.split(".")[0])
        position = int(index.split(".")[1])
        d = direction
        n = 1
        
        if direction.isupper():
            d = direction.lower()
            n = 5
        
        if d == "u":
            text_widget.mark_set('insert',f'{line-n}.{position}')
        elif d == "d":
            text_widget.mark_set('insert',f'{line+n}.{position}')
        elif d == "r":
            text_widget.mark_set('insert',f'insert + {n}c')
        elif d == "l":
            text_widget.mark_set('insert',f'insert - {n}c')
        else:
            return 'break'
        text_widget.see("insert")
        return 'break'
        
    text_widget.bind('<Control-i>', lambda e: mv_cursor(text_widget,'u'))
    text_widget.bind('<Control-k>', lambda e: mv_cursor(text_widget,'d'))
    text_widget.bind('<Control-l>', lambda e: mv_cursor(text_widget,'r'))
    text_widget.bind('<Control-j>', lambda e: mv_cursor(text_widget,'l'))
    text_widget.bind('<Control-Shift-I>', lambda e: mv_cursor(text_widget,'U'))
    text_widget.bind('<Control-Shift-K>', lambda e: mv_cursor(text_widget,'D'))
    text_widget.bind('<Control-Shift-L>', lambda e: mv_cursor(text_widget,'R'))
    text_widget.bind('<Control-Shift-J>', lambda e: mv_cursor(text_widget,'L'))
                
    # Undo Redo
    text_widget.bind('<Control-Shift-Z>', lambda e: text_widget.edit_redo())
    
    # delete line
    def delete_current_line(text_widget):
        # 現在のカーソル位置を取得
        current_index = text_widget.index("insert")
        # 現在の行の開始と終了位置を取得
        line_start = current_index + " linestart"
        line_end = current_index + " lineend + 1c" # 行の終わりの改行文字も含めて削除する
        # 指定された範囲のテキストを削除
        text_widget.delete(line_start, line_end)
        text_widget.mark_set('insert','insert lineend')

        return 'break'
    text_widget.bind('<Shift-BackSpace>', lambda e: delete_current_line(text_widget))
    
    # コロン・行末の位置まで移動
    def get_current_line_text(text_widget):
        # 開始と終了位置のテキストを取得
        tk_index = text_widget.index("insert")
        line = int(tk_index.split(".")[0])
        pos = int(tk_index.split(".")[1])
        line_start = tk_index + " linestart"
        line_end = tk_index + " lineend"
        text = text_widget.get(line_start, line_end)
        
        colon_pos = text.find(':')
        if colon_pos != -1:
            if pos == colon_pos+1:
                text_widget.mark_set('insert',f'{line}.end')
            else:
                text_widget.mark_set('insert',f'{line}.{colon_pos+1}')
        else:
            text_widget.mark_set('insert',f'{line}.end')
        text_widget.see('insert')
        return 'break'
    
    text_widget.bind('<Tab>', lambda e: get_current_line_text(text_widget))
    
    text_widget.pack(fill='both',expand=True)
    
    # 保存ボタンの作成
    save_button = ctk.CTkButton(root, text="Save", command=lambda: save_text(save_filepath, text_widget))
    save_button.pack(fill='x')
        
    def ctrl_s(e):
        print(save_filepath)
        if e.keysym == 's' and e.state & 0x0004:  # Ctrl + S
            save_text(save_filepath, text_widget)
            return "break"
        
    root.bind('<Control-s>', ctrl_s)
    
    return root


# メイン
if __name__ == "__main__":
    global current_index
    current_index = 0
    directory = Path(sys.argv[1])  # 音声ファイルが格納されたディレクトリを指定
    if len(sys.argv) > 2:
        text_file = Path(sys.argv[2])
    else:
        text_file = None
    app = create_app(directory,text_file)
    app.mainloop()
