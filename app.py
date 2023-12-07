# 必要なライブラリのインストール
# pip install Flask moviepy

from flask import Flask, request
from flask import Flask
from moviepy.editor import AudioFileClip
import requests
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'bbbbb'

# MP3音声ファイルのダウンロード
def download_mp3(mp3_url, mp3_filename):
    response = requests.get(mp3_url)
    with open(mp3_filename, 'wb') as file:
        file.write(response.content)

@app.route('/convert', methods=['GET'])
def convert_mp3_to_mp4():
    try:
        # MP3音声ファイルのURLを取得
        base_url = "https://drive.google.com/uc?id="
        drive_id = request.args.get('drive_id')
        file_name = request.args.get('file_name')

        mp3_url = f"{base_url}{drive_id}"
        mp3_file_name = f"{file_name}.mp3"
        mp4_file_name = f"{file_name}.mp4"

        # ダウンロード先のディレクトリにあるすべての.mp3および.mp4ファイルを削除
        for file_name in os.listdir('.'):
            if file_name.endswith('.mp3') or file_name.endswith('.mp4'):
                os.remove(file_name)

        # MP3ファイルをダウンロードして、一時的に保存
        # download_mp3(mp3_url, mp3_file_name)
        # os.system(f'curl -o {mp3_file_name} {mp3_url}')
        subprocess.run(['curl', '-o', mp3_file_name, mp3_url], check=True)

        # ファイルが正常にダウンロードされたかどうかを確認
        if os.path.isfile(mp3_file_name):
            print(f'MP3ファイルがダウンロードされました: {mp3_file_name}')
        else:
            print('MP3ファイルのダウンロードに失敗しました')
        
        # MP3をMP4に変換
        audio_clip = AudioFileClip(mp3_file_name)
        audio_clip.write_videofile(mp4_file_path, codec='libx264', audio_codec='aac')

        # 変換が完了したら一時ファイルを削除
        os.remove(mp3_file_name)

        # ダウンロード可能なURLを生成
        download_url = f'http://aaaa.com/{mp4_file_name}'
        # return jsonify({'download_url': download_url})
        return f'Success: {download_url}'

    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)

