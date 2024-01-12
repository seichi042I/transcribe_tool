from typing import Union,Dict,Callable,List
import os
import threading

import tkinter as tk
from pydub import AudioSegment
from pydub.playback import play
from pathlib import Path



class AudioManager:
    def __init__(self,parent:tk.Widget,wav_dirpath:Path,opts):
        self.wav_list:List = [(wav_dirpath / f) for f in os.listdir(wav_dirpath) if f.endswith('.wav')]
        self.listbox:tk.Listbox = tk.Listbox(parent,**opts)
        self.current_index:int = 0
        
        for file in self.wav_list:
            self.listbox.insert(tk.END, file)
    def next(self):
        self.current_index += 1
        return
    
    def back(self):
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = 0
        return
    
    def set(self,i:int):
        self.current_index = i
        return
        
    # ファイルを再生（スレッドで実行）
    def play(self):
        def run():
            self.current_audio = AudioSegment.from_file(self.wav_list[self.current_index])
            play(self.current_audio)

        thread = threading.Thread(target=run)
        thread.start()
    
    def on_select_item(self):
        self.current_index = self.listbox.curselection()[0]
        self.play()
        return 'break'
        
        
    def play_previous(self,args:Dict = {}):
        if self.wav_list:  # リストが空でないことを確認
            self.back()
            
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            
            self.play()
        return "break"

    def play_current(self,args:Dict = {}):
        if self.wav_list:
            if args['current_cursor_position']:
                self.current_index = args['current_cursor_position']
            self.play()
        return "break"

    def play_next(self,args:Dict = {}):
        if self.wav_list:  # リストが空でないことを確認
            self.next()
            
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            
            self.play()
        return "break"