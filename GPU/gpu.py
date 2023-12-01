#!/usr/bin/python3

from apscheduler.schedulers.background import BlockingScheduler
import ImageProcess, codec
import socket as sock
import struct, time, os, sys

PORT = 9258
HOST = "47.99.113.188"
MSG_SIZE = 128
INTERVAL = 20*60
TIME_FORMATE = "%Y-%m-%d-%H-%M"
ROOM_LIST = ["7201", "7301"]

def sock_init():
    client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    return client

def create_image_dir():
    if not os.path.exists("./image"):
        os.mkdir("./image")
    for room in ROOM_LIST:
        if not os.path.exists("./image/%s" % room):
            os.mkdir("./image/%s" % room)
        if not os.path.exists("./image/%s" % room):
            os.mkdir("./image/%s" % room)
    for room in ROOM_LIST:
        if not os.path.exists("./image/%s/ptz" % room):
            os.mkdir("./image/%s/ptz" % room)
        if not os.path.exists("./image/%s/panorama" % room):
            os.mkdir("./image/%s/panorama" % room)



def cron_job():

    file = open("./nohup.out", "a+")
    sys.stdout = file

    times, connected = 0, False
    #Set the connection of the server
    while False == connected:
        try:
            client = sock_init()
            client.connect((HOST, PORT))
            connected = True
        except sock.error as msg:
            print(msg)
            time.sleep(2)
            times += 1
            if 3 == times:
                sys.exit()


    #### Set the recept request ####
    frame = codec.encode_send(type='recv')
    client.send(frame.encode('utf-8'))

    frame = client.recv(MSG_SIZE)
    frame = bytes.decode(frame)
    roomnums = codec.decode(frame=frame)

    photos = 0
    for n in range(roomnums):
        frame = client.recv(MSG_SIZE)
        frame = bytes.decode(frame)
        room = codec.decode(frame=frame)

        frame = codec.encode_send(type='ok')
        client.send(frame.encode('utf-8'))

        frame = client.recv(MSG_SIZE)
        frame = bytes.decode(frame)
        imgs = codec.decode(frame)

        photos += imgs

        frame = codec.encode_send(type='ok')
        client.send(frame.encode('utf-8'))

        #### Receive the imgs pictures ####
        dirname = time.strftime(TIME_FORMATE, time.localtime(time.time()))
        # print(imgs)
        for num in range(imgs):
            filesize = struct.calcsize('128sq')
            buf = client.recv(filesize)
            if buf:
                # print(len(buf))
                filename, filesize = struct.unpack('128sq', buf)
                ImageProcess.img_get(client, filename, dirname, filesize, room)
        time.sleep(1)

    #### ACK signal from server ####
    frame = client.recv(MSG_SIZE)
    frame = bytes.decode(frame)
    if True == codec.decode(frame=frame):
        print("%s, GPU get %d images!" % (time.asctime(), photos))
    client.close()

def is_timein(timestr:str):
    hour = int(timestr.split(':')[0])
    if 7 <= hour <= 22:
        return True
    else:
        return False

if "__main__" == __name__:

    create_image_dir()
    time.sleep(3)

    current_time = time.strftime(TIME_FORMATE, time.localtime(time.time()))
    while True == is_timein(current_time):
        cron_job()
        time.sleep(INTERVAL)
        current_time = time.strftime(TIME_FORMATE, time.localtime(time.time()))

    schedulers = BlockingScheduler(timezone='MST')
    schedulers.add_job(func=cron_job, trigger="cron", minute="*/20", hour="7-22")
    schedulers.start()
