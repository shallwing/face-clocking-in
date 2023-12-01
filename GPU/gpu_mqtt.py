import socket
import select
import threading
import time
import os
import pandas as pd
import pymysql
import random
import datetime
import struct
import paho.mqtt.client as mqtt
# import cv2

CAMERA = "169.254.68.133"

class Mqtt():
    def __init__(self):
        self.HOST = '47.99.113.188'
        self.PORT = 1883
        self.MSG_SIZE = 128
        self.TIME_INTERVAL = 600
        self.TIME_FORMATE = "%Y-%m-%d-%H-%M"
        self.TOPICALL = "communication/#"
        self.TOPIC1 = "communication/server_to_gpu"
        self.TOPIC2 = "communication/gpu_to_server"
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
        if msg.topic == self.TOPIC1:
            if not os.path.exists(self.picture_path):
                os.mkdir(self.picture_path)
            # Save image
            f = open(self.picture_path + "/1.jpg", 'wb')
            # cv2.imwrite(path + "/%s.jpg" % (time.time()), picture)
            f.write(msg.payload)
            f.close()


    def push_server(self, client, msg):
        client.publish(self.TOPIC2, payload=msg, qos=0)

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
    MQTT.push_server(client, CAMERA + '_left')
    MQTT.push_server(client, CAMERA+'_capture')