import socket
import select
import threading
import time
import pandas as pd
import pymysql
import random
import datetime
import struct
import paho.mqtt.client as mqtt
import os


class Mqtt():
    def __init__(self):
        self.HOST = '47.99.113.188'
        self.PORT = 1883
        self.MSG_SIZE = 128
        self.TIME_INTERVAL = 600
        self.TIME_FORMATE = "%Y-%m-%d-%H-%M"
        self.TOPICALL = 'communication/#'
        self.TOPIC1 = 'communication/server_to_gpu'
        self.TOPIC2 = "communication/gpu_to_server"
        self.TOPIC3 = "communication/raspi_to_server"
        self.TOPIC4 = "communication/server_to_raspi"
        self.picture_path = "./camera_photo/"
        self.message = []
        if not os.path.exists(self.picture_path):
            os.mkdir(self.picture_path)

    def Init_mqtt(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.HOST, self.PORT, self.TIME_INTERVAL)  # 600为keepalive的时间间隔
        return client

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code: " + str(rc))

    def on_message(self, client, userdata, msg):
        # print(msg.topic + " " + str(msg.payload))

        # Processing image
        if msg.topic == self.TOPIC3:
            if not os.path.exists(self.picture_path):
                os.mkdir(self.picture_path)
            # Save image
            save_path = self.picture_path + "/%s.jpg" % (time.time())
            f = open(save_path, 'wb')
            # cv2.imwrite('../picture/container_picture/%d-%d-%d-%s.jpg' %(address ,floor ,number ,time), picture)
            f.write(msg.payload)
            f.close()
            self.push_gpu(client,save_path)

        elif msg.topic == self.TOPIC2:
            self.push_raspi(client,msg.payload)

        # dirname = time.strftime(self.TIME_FORMATE, time.localtime(time.time()))
        #
        # filesize = struct.calcsize('128sq')
        #
        # # print(len(buf))
        # filename, filesize = struct.unpack('128sq', msg)
        #
        # ImageProcess.img_get(client, filename, dirname, filesize, room)

    def push_gpu(self, client, msg_dir):
        f = open(msg_dir, 'rb')
        filedata = f.read()
        byteArr = bytes(filedata)
        # client.publish(self.TOPIC1, payload=room, qos=0)
        client.publish(self.TOPIC1, payload=byteArr, qos=0)

    def push_raspi(self, client, msg):
        client.publish(self.TOPIC4, payload=msg, qos=0)

    def Subscribe_Topic(self, client):
        client.subscribe(self.TOPICALL, qos=0)
        client.loop_forever()  # 保持连接

    def start_server(self, client):
        t1 = threading.Thread(target=self.Subscribe_Topic, args=(client,))
        t1.start()


if __name__ == '__main__':
    MQTT = Mqtt()
    client = MQTT.Init_mqtt()
    MQTT.start_server(client)