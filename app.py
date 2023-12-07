# 必要なライブラリのインストール
# pip install Flask moviepy

from flask import Flask, request
from flask import Flask
from moviepy.editor import AudioFileClip

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Worldaaaaaa!'

@app.route('/convert', methods=['GET'])
def convert_mp3_to_mp4():
    try:
        # MP3音声ファイルのURLを取得
        mp3_url = request.args.get('mp3_url')

        # MP3ファイルをダウンロードして、一時的に保存
        mp3_file_path = 'temp.mp3'
        # ここにダウンロード処理を追加

        # MP3をMP4に変換
        mp4_file_path = mp3_file_path.replace('.mp3', '.mp4')
        audio_clip = AudioFileClip(mp3_file_path)
        audio_clip.write_videofile(mp4_file_path, codec='libx264', audio_codec='aac')

        # 変換が完了したら一時ファイルを削除
        # ここにファイル削除処理を追加

        return f'Success: {mp4_file_path}'

    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)

