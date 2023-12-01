#!/usr/bin/python3
import sys

from apscheduler.schedulers.background import BlockingScheduler
import ImageProcess, codec
from PTZControl import *
import socket as sock
import os, time

## The number of pre-points 
NUM = 1

#ROOM = "7201"
ROOM = "7301"
PORT = 9258
HOST = "47.99.113.188"
MSG_SIZE = 128
#CAMERA = "169.254.230.144"
CAMERA = "169.254.68.133"

TIME_FORMATE = "%H:%M"


def sock_init():
    client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    return client

'''Set by reality'''
def capture_process():
    for i in range(NUM):
        preset_point(position=i+1, address=CAMERA)
        time.sleep(10)
        capture_photo(address=CAMERA, pos=i+1, channel=1)



def cron_job():

    cwd = os.path.dirname(os.path.abspath(__file__))

    file = open("%s/nohup.out" % cwd, "a+")
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

    if not os.path.exists("%s/camera_photo" % cwd):
        os.mkdir("%s/camera_photo" % cwd)
    if not os.path.exists("%s/camera_photo/ptz" % cwd):
        os.mkdir("%s/camera_photo/ptz" % cwd)
    if not os.path.exists("%s/camera_photo/panorama" % cwd):
        os.mkdir("%s/camera_photo/panorama" % cwd)

    capture_process()

    #### Send images from server ####
    pan = os.listdir("%s/camera_photo/panorama" % cwd)
    ptz = os.listdir("%s/camera_photo/ptz" % cwd)

    frame = codec.encode_send(room=ROOM, type='room')
    client.send(frame.encode('utf-8'))

    frame = client.recv(MSG_SIZE)
    frame = bytes.decode(frame)
    if codec.decode(frame=frame):
        frame = codec.encode_send(count=len(pan) + len(ptz), type='count')
        client.send(frame.encode('utf-8'))

    frame = client.recv(MSG_SIZE)
    frame = bytes.decode(frame)
    if codec.decode(frame=frame):
        for filename in ptz + pan:
            fhead = ImageProcess.img_pack(filename)
            client.send(fhead)
            ImageProcess.img_send(filename, client)
            time.sleep(2)
    #### ACK signal to server ####
    frame = client.recv(MSG_SIZE)
    frame = bytes.decode(frame)
    if codec.decode(frame=frame):
        client.close()




if '__main__' == __name__:

    from apscheduler.schedulers.background import BlockingScheduler
    time.sleep(1*60)

    schedulers = BlockingScheduler(timezone='Asia/Shanghai')
    schedulers.add_job(func=cron_job, trigger="cron", max_instances=4, day_of_week="mon-sun", second="40", minute="19,39,59", hour="7-22")
    schedulers.start()

