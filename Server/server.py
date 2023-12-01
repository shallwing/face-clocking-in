#!/usr/bin/python3

#-*- coding : utf-8-*-
# coding:unicode_escape

import socket as sock
import struct, os, time
import ImageProcess, codec

PORT = 9258
BACK_LOG = 32
MSG_SIZE = 128
TIME_FORMATE = "%Y-%m-%d-%H-%M"
ROOM_LIST = ["7201", "7301"]


def sock_init():
    server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    server.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
    hostname = sock.gethostname()
    server.bind((hostname, PORT))
    server.listen(BACK_LOG)
    return server

def create_image_dir():
    if not os.path.exists("./camera_photo"):
        os.mkdir("./camera_photo")
    for room in ROOM_LIST:
        if not os.path.exists("./camera_photo/%s" % room):
            os.mkdir("./camera_photo/%s" % room)
        if not os.path.exists("./camera_photo/%s" % room):
            os.mkdir("./camera_photo/%s" % room)
    for room in ROOM_LIST:
        if not os.path.exists("./camera_photo/%s/ptz" % room):
            os.mkdir("./camera_photo/%s/ptz" % room)
        if not os.path.exists("./camera_photo/%s/panorama" % room):
            os.mkdir("./camera_photo/%s/panorama" % room)

def get_room_list():
    roomlist = []
    for room in ROOM_LIST:
        pandir = "./camera_photo/%s/panorama" % room
        ptzdir = "./camera_photo/%s/ptz" % room
        pan, ptz = os.listdir(pandir), os.listdir(ptzdir)
        if len(pan) or len(ptz):
            roomlist.append(room)
    return roomlist



if "__main__" == __name__:

    create_image_dir()

    server = sock_init()
    count =  0


    while True:
        client, address = server.accept()
        frame = client.recv(MSG_SIZE)
        frame = bytes.decode(frame)
#### When Raspi connect the server, receive pictures from it ####
        if frame.find("Pi") >= 0:

            room = codec.decode(frame=frame)

            frame = codec.encode_send(type='ok')
            client.send(frame.encode('utf-8'))

            frame = client.recv(MSG_SIZE)
            frame = bytes.decode(frame)
            count = codec.decode(frame=frame)
            dirname = time.strftime(TIME_FORMATE, time.localtime(time.time()))

            frame = codec.encode_send(type='ok')
            client.send(frame.encode('utf-8'))

            for num in range(count):
                filesize = struct.calcsize('128sq')
                buf = client.recv(filesize)
                if buf:
                    #print(len(buf))
                    filename, filesize = struct.unpack('128sq', buf)
                    ImageProcess.img_get(client, filename, dirname, filesize, room)

#### Send ACK signal to Raspi ####
            frame = codec.encode_send(type='ok')
            client.send(frame.encode('utf-8'))
            client.close()
            buf = []


#### When GPU connect the server, send pictures to GPU ####
        if frame.find("GPU") >= 0:
            if 'recv' == codec.decode(frame=frame):
                    roomlist = get_room_list()
                    frame = codec.encode_send(type='roomnums', rooms=len(roomlist))
                    client.send(frame.encode('utf-8'))


                    for room in roomlist:

                        frame = codec.encode_send(type='room', room=room)
                        client.send(frame.encode('utf-8'))

                        frame = client.recv(MSG_SIZE)
                        frame = bytes.decode(frame)
                        if True == codec.decode(frame=frame):
                            print("The GPU host has received the room ID.\n")

                        pandir, ptzdir = "./camera_photo/%s/panorama" % room, "./camera_photo/%s/ptz" % room
                        pan, ptz = os.listdir(pandir), os.listdir(ptzdir)
                        #print(ptz)
                        if pan:
                            pandir = sorted(pan, key=lambda x: os.path.getmtime(os.path.join(pandir, x)))
                            pandir = pandir[-1]
                            pan = os.listdir("./camera_photo/%s/panorama/%s" % (room, pandir))

                        if ptz:
                            ptzdir = sorted(ptz, key=lambda x: os.path.getmtime(os.path.join(ptzdir, x)))
                            ptzdir = ptzdir[-1]
                            ptz = os.listdir("./camera_photo/%s/ptz/%s" % (room, ptzdir))

                        frame = codec.encode_send(count=len(pan) + len(ptz), type='count')
                        client.send(frame.encode('utf-8'))

                        frame = client.recv(MSG_SIZE)
                        frame = bytes.decode(frame)
                        if codec.decode(frame=frame):
                            for filename in ptz:
                                fhead = ImageProcess.img_pack(filename, ptzdir, room)
                                client.send(fhead)
                                ImageProcess.img_send(filename, ptzdir, client, room)
                                time.sleep(2)
                            for filename in pan:
                                fhead = ImageProcess.img_pack(filename, pandir, room)
                                client.send(fhead)
                                ImageProcess.img_send(filename, ptzdir, client, room)
                                time.sleep(2)
                            #time.sleep(2)
#### ACK signal to GPU ####
            frame = codec.encode_send(type='ok')
            client.send(frame.encode("utf-8"))
            client.close()
