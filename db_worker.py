import json
import os
import sys

import gridfs
import pika
from pymongo import MongoClient

rmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = rmq_connection.channel()
channel.queue_declare('photos')

mongo = MongoClient('localhost', 27017)
db = mongo['photo']
fs = gridfs.GridFS(db)


def add_photo(data):
    with open(data['path'], 'rb') as f:
        filename = data['path'].split('/')[-1]
        id_ = fs.put(f, filename=filename)
        print(fs.list())
        print(f'photo putted in db, id {id_}')


def delete_photo(data):
    filename = data['path'].split('/')[-1]
    id_ = fs.find_one(filename)
    fs.delete(id_)
    print('photo deleted from db')


def callback(ch, method, properties, body):
    data = json.loads(body)
    strategies = {'add': add_photo,
                  'delete': delete_photo}
    try:
        action = strategies[data['action']]
    except KeyError:
        print('wrong message')
    action(data)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.basic_consume(queue='photos', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
