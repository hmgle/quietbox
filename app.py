# /usr/bin/env python

from flask import Flask, jsonify
import glob, os, subprocess

app = Flask(__name__)
local_music = []
FIFO = '/tmp/quietbox.fifo'

@app.route('/')
def miao():
    return "miao"


@app.route('/163/<int:list_id>', methods=['GET'])
def get_163(list_id):
    # TODO
    return jsonify({'list': list_id})


@app.route('/local/list', methods=['GET'])
def get_local():
    return jsonify(local_music)

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


try:
    os.mkfifo(FIFO)
except OSError, e:
    print "Failed to create FIFO: %s" % e

if __name__ == '__main__':
    subprocess.Popen(['mpg123', '-R',  '--fifo', FIFO],
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE)
    wfd = os.open(FIFO, os.O_NONBLOCK | os.O_WRONLY)
    load_local()
    app.run()
