import os
import shutil
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import Union

class CorpusFormatter:
    def __init__(self):
        """
        ディレクトリ構造を管理するクラス
        """
    
    def file_tree_format(self,path:Path):
                
        file_list = os.listdir(path.parent)
        
        # 話者ディレクトリを確認or作成
        if path.name == "wav":            
            self.speaker_dirpath = path.parent
            # if "transcript_utf8.txt" in file_list:
            #     self.speaker_dirpath = path.parent
            # else:
            #     count=1
            #     while os.path.exists((path.parent / f"SPEAKER{count}")):
            #         count += 1
            #     os.mkdir((path.parent / f"SPEAKER{count}"))
            #     self.speaker_dirpath = (path.parent / f"SPEAKER{count}")
                
            self.wav_dirpath = path
        elif 'wav' in file_list:
            self.speaker_dirpath = path
            self.wav_dirpath = path / 'wav'
            
        
        # wavディレクトリのファイルをチェック
        filelist = os.listdir(self.wav_dirpath)
        not_wavfiles_filter = filter(lambda file_path: not file_path.endswith('.wav'),filelist)
        not_wavfiles = list(not_wavfiles_filter)
        
        # wavファイル以外を移動
        if not_wavfiles:
            # その他のファイルを入れるディレクトリを作成
            otherfiles_path = (self.speaker_dirpath / "otherfiles")
            otherfiles_path.mkdir(parents=True,exist_ok=True)
            
            # 種類に応じて、ファイルを移動
            for nwf in not_wavfiles:
                nwfpath = Path(nwf)
                distination_path = (otherfiles_path / nwf)
                
                if nwfpath.suffix == '.md':
                    distination_path = (self.speaker_dirpath / nwf)
                elif nwfpath.name in ['transcript_utf8.txt','speaker_total_duration.txt']:
                    if not os.path.exists(self.speaker_dirpath / nwf):
                        distination_path = (self.speaker_dirpath / nwf)
                
                shutil.move((self.wav_dirpath / nwf),distination_path)
            
            # 空だったら削除
            if not os.listdir(otherfiles_path):
                os.rmdir(otherfiles_path)
            
            
            

class DirectoryChooser:
    def __init__(self,widget: Union[tk.Tk, tk.Frame]):
        """
        ディレクトリ選択UIを管理するクラス
        Arguments:
            widget(tk.Tk or tk.Frame):UIをアタッチする親ウィジェット
        Returns:
        """
        self.root = tk.Frame(widget)
        self.directory = ""
        
        # パス入力フィールド
        self.path_entry = tk.Entry(self.root, width=50)
        self.path_entry.grid(row=0, column=0, padx=0, pady=10)

        # ディレクトリ選択ボタン
        self.browse_button = tk.Button(self.root, text="ブラウズ", command=self.browse_directory)
        self.browse_button.grid(row=0, column=1, padx=0, pady=10)
        
    
    def browse_directory(self):
        """
        ブラウズボタンを押したときの処理
        """
        self.directory = Path(filedialog.askdirectory())
        if self.directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, self.directory)
    
    def attach(self):
        self.root.pack()

    def detach(self):
        self.root.pack_forget()



if __name__ == "__main__":
    
    # トップレベルウィンドウの作成
    root = tk.Tk()
    root.title("ディレクトリ選択")

    # DirectoryChooserクラスのインスタンスを作成
    directory_chooser = DirectoryChooser(root)

    # アタッチとデタッチをテストするためのボタン
    attach_button = tk.Button(root, text="アタッチ", command=directory_chooser.attach)
    detach_button = tk.Button(root, text="デタッチ", command=directory_chooser.detach)
    attach_button.pack()
    detach_button.pack()
    
    cf = CorpusFormatter()
    cf.file_tree_format(Path("idolmaster_milion_live/IORI/wav"))

    # イベントループの開始
    root.mainloop()
    
