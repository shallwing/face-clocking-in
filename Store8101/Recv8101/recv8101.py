#!/usr/bin/python3

#-*- coding : utf-8-*-
# coding:unicode_escape

import socket as sock
import struct, os, time
import ImageProcess, codec

PORT = 7358
BACK_LOG = 32
MSG_SIZE = 128
TIME_FORMATE = "%Y-%m-%d-%H-%M"


def sock_init():
    server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    server.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
    hostname = sock.gethostname()
    server.bind((hostname, PORT))
    server.listen(BACK_LOG)
    return server

def create_image_dir():
    cwd = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists("%s/camera_photo" % cwd):
        os.mkdir("%s/camera_photo" % cwd)



if "__main__" == __name__:

    create_image_dir()

    server = sock_init()

    while True:
        client, address = server.accept()

        frame = client.recv(MSG_SIZE)
        frame = bytes.decode(frame)
        count = codec.decode(frame=frame)

        frame = codec.encode_send(type='ok')
        client.send(frame.encode('utf-8'))

        dirname = time.strftime(TIME_FORMATE, time.localtime(time.time()))
        for num in range(count):
            filesize = struct.calcsize('128sq')
            buf = client.recv(filesize)
            print(filesize)
            print(buf)
            if buf:
                filename, filesize = struct.unpack('128sq', buf)
                ImageProcess.img_get(client, filename, dirname, filesize)
            time.sleep(1)

        frame = codec.encode_send(type='ok')
        client.send(frame.encode('utf-8'))

        client.close()
