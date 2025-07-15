from flask import Flask, render_template, request
from pytube import Playlist
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    resolution = request.form['resolution']
    playlist = Playlist(url)

    download_path = os.path.join(os.getcwd(), 'downloads')
    os.makedirs(download_path, exist_ok=True)

    for i, video in enumerate(playlist.videos, start=1):
        stream = video.streams.filter(res=resolution, progressive=True).first()
        if not stream:
            stream = video.streams.get_highest_resolution()
        stream.download(output_path=download_path)
        print(f"{i}. Downloaded: {video.title}")

    return f"✅ Downloaded {len(playlist.video_urls)} videos to /downloads folder!"

if __name__ == '__main__':
    app.run(debug=True)
