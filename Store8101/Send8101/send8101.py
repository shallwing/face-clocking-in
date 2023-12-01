#!/usr/bin/python3

#from apscheduler.schedulers.background import BlockingScheduler
import ImageProcess, codec
import socket as sock
import time, os, sys

PORT = 7358
HOST = "47.99.113.188"
MSG_SIZE = 128
PATH = "/home/lwj/data/picture"

def sock_init():
    client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    return client


def cron_job():

#    file = open("./nohup.out", "a+")
#    sys.stdout = file

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

    dirname = sorted(os.listdir(PATH), key=lambda x: os.path.getmtime(os.path.join(PATH, x)))
    dirname = dirname[-1]
    imgs = os.listdir(PATH + "/%s" % dirname)
    

    frame = codec.encode_send(type='count', count=len(imgs))
    client.send(frame.encode('utf-8'))

    frame = client.recv(MSG_SIZE)
    frame = bytes.decode(frame)
    if True == codec.decode(frame=frame):
        time.sleep(1)
        for filename in imgs:
            fhead = ImageProcess.img_pack(filename, dirname)
            print(fhead)
            client.send(fhead)
            ImageProcess.img_send(filename, dirname, client)


    frame = client.recv(MSG_SIZE)
    frame = bytes.decode(frame)
    if True == codec.decode(frame=frame):
        pass
    else:
        cur_time = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        print("%s, fail to send the 8101's photos to Aliyun server!" % cur_time)
    client.close()

if "__main__" == __name__:

    #schedulers = BlockingScheduler(timezone='Asia/Shanghai')
    #schedulers.add_job(func=cron_job, day_of_week="mon-sun", trigger="cron", second="15", minute="0, 20, 40", hour="8-22")
    #schedulers.start()

    while True:
        cron_job()
        time.sleep(5)
