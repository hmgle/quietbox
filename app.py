# /usr/bin/env python
# coding: utf-8

from flask import Flask, jsonify
import glob, os, subprocess
import NEMbox
from time import sleep

app = Flask(__name__)
local_musics = []
FIFO = '/tmp/quietbox.fifo'
nbox = NEMbox.api.NetEase()

def get_163_playlist(playlist_id):
    songs = nbox.playlist_detail(playlist_id)
    detail_list = nbox.dig_info(songs, 'songs')
    playlist = []
    for e in detail_list:
        playlist.append({"id": e['song_id'], "name": e['song_name']})
    return playlist


def get_163_song_url(song_id):
    song = nbox.songs_detail_new_api([song_id])
    return song[0]['url']


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/163/<int:list_id>', methods=['GET'])
def get_163(list_id):
    return jsonify({'musics': get_163_playlist(list_id)})


@app.route('/local/list', methods=['GET'])
def get_local():
    return jsonify({'musics': local_musics})


@app.route('/local/play/<int:id>', methods=['GET'])
def local_play(id):
    for item in local_musics:
        if item["id"] == id:
            file_path = item["name"]
            os.write(wfd, "\nL " + file_path + "\n")
            return "ok"
    return "not found"


@app.route('/163/play/<int:id>', methods=['GET'])
def wangye_play(id):
    song_url = get_163_song_url(id)
    if song_url is not None:
        os.write(wfd, "\nL " + song_url + "\n")
        return "ok"
    return "not found"


def load_local():
    for file in glob.glob("*.mp3"):
        local_musics.append({"id": len(local_musics),  "name": file})



if __name__ == '__main__':
    try:
        os.mkfifo(FIFO)
    except OSError, e:
        print "Failed to create FIFO: %s" % e
    subprocess.Popen(['mpg123', '-R',  '--fifo', FIFO])
    sleep(0.1)
    wfd = os.open(FIFO, os.O_NONBLOCK | os.O_WRONLY)
    load_local()
    app.run(host='0.0.0.0', port=8888)
