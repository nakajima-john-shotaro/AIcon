import argparse
import hashlib
import pathlib
import json
import os
import sys
import datetime
import time
import threading
import shutil
from natsort import natsorted

from imageio import imread, mimsave

import requests
from flask import Flask, jsonify, redirect, render_template, request
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from googletrans import Translator

from big_sleep import Imagine as BigImagine
from deep_daze import Imagine as DeepImagine

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False
CORS(app)

dst_img_dir = '../../frontend/src/static/dst_img'
dst_gif_dir = '../../frontend/src/static/dst_gif'
sess_dir_path = './sess_abt'

translator = Translator()
client_data = {}

@app.route("/data", methods=["POST"])
def aicon():
    json_data = request.get_json()

    hash_id = json_data["hash"]

    if hash_id == "000000000000":
        dt = datetime.datetime.now()
        dt_ts = str(dt.timestamp())
        hash_id = hashlib.sha256(dt_ts.encode()).hexdigest()
        client_data[hash_id] = False
        json_data["hash"] = hash_id
        json_data["is_finish"] = client_data[hash_id]

        print(f'Hash: {hash_id}')

        os.makedirs(os.path.join(dst_img_dir, hash_id), exist_ok=True)
        os.makedirs(os.path.join(dst_gif_dir, hash_id), exist_ok=True)
        os.makedirs(sess_dir_path, exist_ok=True)
        sess_path = hash_id + '.sess'
        with open(os.path.join(sess_dir_path, sess_path), 'w'):
            pass

        input_text = json_data["text"]
        json_data["text"] = translate(input_text)

        file_path = get_path(hash_id, json_data)
        json_data["path"] = file_path

        thread = threading.Thread(target=run_model, args=(json_data, ))
        thread.start()

        remove_dir()
        return jsonify(json_data)
    
    if hash_id in client_data:
        if json_data["abort"]:
            client_data[hash_id] = True

        if client_data[hash_id]:
            json_data["is_finish"] = client_data[hash_id]
            json_data["path"] = get_path(hash_id, json_data)
            json_data["gif_path"] = generate_gif(hash_id)
            json_data["ittr"] = get_progress(hash_id, json_data)[0]
            json_data["total_ittr"] = json_data["iterations"]
            
            del client_data[hash_id]
            sess_path = hash_id + '.sess'
            try:
                os.remove(os.path.join(sess_dir_path, sess_path))
            except FileNotFoundError:
                pass
            return jsonify(json_data)
        else:
            json_data["is_finish"] = client_data[hash_id]
            json_data["path"] = get_path(hash_id, json_data)
            json_data["gif_path"] = 'cant_save_gif.err'
            json_data["ittr"] = get_progress(hash_id, json_data)[0]
            json_data["total_ittr"] = json_data["iterations"]
            return jsonify(json_data)

    return jsonify({"message": "Forbidden: You Don't Have a Valid ID"}), 403

def generate_gif(hash_id):
    images = []
    for i, file_name in enumerate(sorted(os.listdir(os.path.join(dst_img_dir, hash_id)))):
        if i % 2 == 0:
            images.append(imread(os.path.join(os.path.join(dst_img_dir, hash_id), file_name)))
    if len(images) < 2:
        return 'cant_save_gif.err'
    mimsave(f'{dst_gif_dir}/{hash_id}/{hash_id}.gif', images, 'GIF')
    ret_path = 'static/dst_gif/' + hash_id + '/' + hash_id + '.gif'
    return ret_path

def get_progress(hash_id, json_data):
    img_dir = os.path.join(dst_img_dir, hash_id)
    iterations = int(sum(os.path.isfile(os.path.join(img_dir, name)) for name in os.listdir(img_dir)))
    total_iterations = json_data["iterations"] * json_data["epochs"]

    return iterations, total_iterations
    
def remove_dir():
    files = os.listdir(dst_img_dir)
    dir_list  = [f for f in files if os.path.isdir(os.path.join(dst_img_dir, f))]
    for dir_name in dir_list:
        creation_time = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(dst_img_dir, dir_name)))
        time_delta = datetime.datetime.now() - creation_time
        if time_delta.total_seconds() > 900 and dir_name not in client_data:
            shutil.rmtree(os.path.join(dst_img_dir, dir_name))
            print(f'Deleted following dir due to timeout: {os.path.join(dst_img_dir, dir_name)}', file=sys.stderr)

    files = os.listdir(dst_gif_dir)
    dir_list  = [f for f in files if os.path.isdir(os.path.join(dst_gif_dir, f))]
    for dir_name in dir_list:
        creation_time = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(dst_gif_dir, dir_name)))
        time_delta = datetime.datetime.now() - creation_time
        if time_delta.total_seconds() > 900:
            shutil.rmtree(os.path.join(dst_gif_dir, dir_name))
            print(f'Deleted following dir due to timeout: {os.path.join(dst_gif_dir, dir_name)}', file=sys.stderr)

def get_path(hash_id, json_data):
    if json_data["model_name"] == "deep_daze":
        ext = '.jpg'
    else:
        ext = '.png'
    img_dir = os.path.join(dst_img_dir, hash_id)
    img_paths = [p for p in pathlib.Path(img_dir).iterdir() if p.is_file()]
    num_file = len(list(img_paths))
    if num_file < 2:
        return 'img_not_generated_yet.err'
    else:
        file_path = list(reversed(natsorted(img_paths)))
        return 'static/dst_img/' + hash_id + '/' + os.path.basename(file_path[1])

def run_model(json_data):
    model_name = json_data["model_name"]

    if model_name == "deep_daze":
        deep_daze(json_data)
            
    elif model_name == "big_sleep":
        big_sleep(json_data)
    else:
        return jsonify({"message": "Internal Error: No Such Model Name"}), 500

def deep_daze(json_data):
    imagine = DeepImagine(
        text=json_data["text"],
        image_width=json_data["image_width"],
        save_every=json_data["save_every"],
        epochs=json_data["epochs"],
        iterations=json_data["iterations"],
        num_layers=44,
        batch_size=32,
        gradient_accumulate_every=1,
        # start_image_path="../src_img/input.jpg",
        save_dir=dst_img_dir + '/' + str(json_data["hash"]),
        hash_id=json_data["hash"],
    )

    client_data[json_data["hash"]] = imagine()


def big_sleep(json_data):
    imagine = BigImagine(
        text=json_data["text"],
        image_size=json_data["image_width"],
        save_every=json_data["save_every"],
        epochs=json_data["epochs"],
        iterations=json_data["iterations"],
        lr=0.07,
        save_progress=True,
        save_dir=dst_img_dir + '/' + str(json_data["hash"]),
        hash_id=json_data["hash"],
    )

    client_data[json_data["hash"]] = imagine()


def translate(input_text):
    input_lang = translator.detect(input_text).lang

    if not input_lang == "en":
        output_text = translator.translate(input_text, src=input_lang, dest="en").text
    else:
        output_text = input_text

    return output_text


def main():
    app.run(host="0.0.0.0", port=8081, threaded=False)


if __name__ == "__main__":
    main()
