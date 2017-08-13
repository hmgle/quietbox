# /usr/bin/env python

from flask import Flask, jsonify
import glob, os, subprocess
from time import sleep

app = Flask(__name__)
local_music = []
FIFO = '/tmp/quietbox.fifo'

@app.route('/')
def index():
    # return render_template('index.html',items=local_music)
    return app.send_static_file('index.html')


@app.route('/163/<int:list_id>', methods=['GET'])
def get_163(list_id):
    # TODO
    return jsonify({'list': list_id})


@app.route('/local/list', methods=['GET'])
def get_local():
    return jsonify({'musics': local_music})

@app.route('/local/play/<int:id>', methods=['GET'])
def local_play(id):
    for item in local_music:
        if item["id"] == id:
            file_path = item["name"]
            os.write(wfd, "\nL " + file_path + "\n")
            return "ok"
    return "not found"


def load_local():
    for file in glob.glob("*.mp3"):
        local_music.append({"id": len(local_music),  "name": file})



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
