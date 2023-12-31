# 必要なライブラリのインストール
# pip install Flask moviepy

from flask import Flask, request, jsonify, send_file
# from flask import Flask
#from moviepy.editor import AudioFileClip
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
import requests
import os
import subprocess
import time
import magic

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

        image_file_name = "input_image.jpeg"

        # ダウンロード先のディレクトリにあるすべての.mp3および.mp4ファイルを削除
        for file_name in os.listdir('.'):
            if file_name.endswith('.mp3') or file_name.endswith('.mp4'):
                os.remove(file_name)

        
        # MP3ファイルをダウンロードして、一時的に保存
        print(f'mp3_url: {mp3_url}')
        download_mp3(mp3_url, mp3_file_name)
        # os.system(f'curl -o {mp3_file_name} {mp3_url}')
        # subprocess.run(['curl', '-o', mp3_file_name, mp3_url], check=True)
        #download_process = subprocess.run(['curl', '-o', mp3_file_name, mp3_url], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 10秒間待機
        #time.sleep(20)

        # ダウンロード先のディレクトリにあるすべてのファイルを一覧表示
        all_files = os.listdir('.')
        print('ダウンロード先のディレクトリにあるすべてのファイル:')
        for file_name in all_files:
            print(file_name)
        
        # ダウンロードが正常に終了したかどうかを確認
        #if download_process.returncode == 0:
        #    print(f'MP3ファイルがダウンロードされました: {mp3_file_name}')
        #    result = 'success'

        #else:
        #    print('MP3ファイルのダウンロードに失敗しました')
        #    print('エラーメッセージ:', download_process.stderr.decode())
        #    result = 'fail'
        
        # ファイルが正常にダウンロードされたかどうかを確認
        #if os.path.isfile(mp3_file_name):
        #    print(f'MP3ファイルがダウンロードされました: {mp3_file_name}')
        #else:
        #    print('MP3ファイルのダウンロードに失敗しました')

        # python-magic モジュールでMIMEタイプを取得
        print(f'python-magic for mp3_file_name: {magic.from_file(mp3_file_name, mime=True)}')
        
        # return jsonify({'files': all_files})
        download_url = f'https://convert-mp3-to-mp4.onrender.com/{mp3_file_name}'
        #return jsonify({'download_url': download_url})
        # return jsonify({'download_url': download_url})
        
        # mp3音声ファイルをそのまま返してみる
        # return send_file(mp3_file_name, as_attachment=True,
        #                 #attachment_filename=mp3_file_name,
        #                 mimetype='audio/mpeg')
        #return result

        # MP3音声ファイルを読み込む
        audio_clip = AudioFileClip(mp3_file_name)

        # 画像ファイルを読み込んでビデオクリップを作成
        image_clip = ImageClip(image_file_name, duration=audio_clip.duration)

        # 音声と画像を結合してビデオクリップを作成
        video_clip = CompositeVideoClip([image_clip.set_duration(audio_clip.duration).set_audio(audio_clip)])

        # ビデオをファイルに書き出す
        video_clip.write_videofile(mp4_file_name, codec='libx264', audio_codec='aac', fps=24)

        # python-magic モジュールでMIMEタイプを取得
        print(f'python-magic for mp4_file_name: {magic.from_file(mp4_file_name, mime=True)}')

        # 変換が完了したら一時ファイルを削除
        os.remove(mp3_file_name)

        # ダウンロード可能なURLを生成
        #download_url = f'https://convert-mp3-to-mp4.onrender.com/{mp4_file_name}'
        # return jsonify({'download_url': download_url})
        #return f'Success: {download_url}'
        return send_file(mp4_file_name, as_attachment=True,
                         download_name=mp4_file_name,
                         mimetype='video/mpeg')
    
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)

