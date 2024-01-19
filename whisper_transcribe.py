import os
import sys
from pathlib import Path
from turtle import mode
import whisper
from tqdm import tqdm

def recurrent_transcribe(directory:Path, model_size:str = 'large-v3'):
    """指定されたディレクトリ以下のすべてのWAVファイルを文字起こしする"""
    model = whisper_transcribe.load_model(model_size)

    for root, dirs, files in os.walk(directory):
        rootpath = Path(root)
        if rootpath.name != 'wav':
            continue
        print(f"processing {rootpath}")
        with open(rootpath.parent / 'transcript_utf8.txt','w',encoding='utf-8') as f:
            for file in tqdm(files):
                filepath = rootpath / Path(file)
                if filepath.suffix == ".wav":
                    result = model.transcribe(str(filepath),language='ja')
                    text = str(filepath.stem)+':'+result['text']+'\n'
                    f.write(text)

if __name__ == "__main__":
    model_size='large-v3'
    rootpath = Path(sys.argv[1])
    recurrent_transcribe(rootpath,model_size)