import json
from uuid import uuid4

import gridfs
import pika
from flask import Flask, jsonify, request, send_file
from pymongo import MongoClient

app = Flask('photo')


def create_connection():
    rmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = rmq_connection.channel()
    channel.queue_declare('photos')
    return channel


mongo = MongoClient('localhost', 27017)
db = mongo['photo']
fs = gridfs.GridFS(db)


def add_to_db(path):
    channel = create_connection()
    channel.basic_publish(exchange='',
                          routing_key='photos',
                          body=json.dumps({'path': path, 'action': 'add'}))


def delete_from_db(path):
    channel = create_connection()
    channel.basic_publish(exchange='',
                          routing_key='photos',
                          body=json.dumps({'path': path, 'action': 'delete'}))


@app.route('/photos', methods=['POST', 'DELETE'])
def handle_photo():
    print('REQUEST')
    if request.method == 'POST':
        result = []
        for k, v in request.files.items():
            name = f'{uuid4()}.jpg'
            path = f'uploads/{name}'
            v.save(path)
            add_to_db(path)
            result.append(name)
        return jsonify(result)
    elif request.method == 'DELETE':
        res = delete_from_db(request.get_json()['name'])
        if res is not None:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'reason': 'No file'})


@app.route('/photos/<photo_name>', methods=['GET'])
def get_photo(photo_name):
    print('REQUEST')
    if request.method == 'GET':
        photo = fs.find_one({'filename': photo_name})
        if photo is not None:
            return send_file(photo,
                             mimetype='image/jpeg',
                             as_attachment=True,
                             attachment_filename=photo_name)

        return jsonify({'success': False, 'reason': 'No file'})
