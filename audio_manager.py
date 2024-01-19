from typing import Union,Dict,Callable,List
import os
import threading

from pydub import AudioSegment
from pydub.playback import play
from pathlib import Path
import random

OWNPATH = Path(__file__)

class AudioManager:
    def __init__(self,wav_dirpath:Path,opts):
        self.wav_dirpath = wav_dirpath
        self.wav_path_list = [(wav_dirpath / f) for f in os.listdir(wav_dirpath) if f.endswith('.wav')]
        self.current_index:int = 0
        self.play_error_sound_list = os.listdir(OWNPATH.parent / "system_voice" / "play_error")
        
    # ファイルを再生（スレッドで実行）
    def play(self,stem):
        name = stem+".wav"
        print((self.wav_dirpath / name))
        def run():
            try:
                self.current_audio = AudioSegment.from_file((self.wav_dirpath / name))
                play(self.current_audio)
            except:
                dir = OWNPATH.parent / "system_voice" / "play_error"
                sound = self.play_error_sound_list[random.randint(0,3)]
                _audio = AudioSegment.from_file(dir/sound)
                play(_audio)

        thread = threading.Thread(target=run)
        thread.start()
        
        return "break"