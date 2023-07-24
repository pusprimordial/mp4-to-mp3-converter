from flask import Flask, render_template, request, redirect
from pytube import YouTube
import os
from flask_frozen import Freezer

app = Flask(__name__)
freezer = Freezer(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        video = YouTube(url)
        audio_stream = video.streams.filter(only_audio=True).first()
        audio_stream.download()

        default_filename = audio_stream.default_filename
        mp3_filename = os.path.splitext(default_filename)[0] + '.mp3'
        os.rename(default_filename, 'static/' + mp3_filename)

        return redirect('/download/' + mp3_filename)

    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/download/<mp3_filename>')
def download_mp3(mp3_filename):
    return render_template('download.html', mp3_filename=mp3_filename)

if __name__ == '__main__':
    app.run(debug=True)
