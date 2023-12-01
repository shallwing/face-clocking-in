import threading
import paho.mqtt.client as mqtt
import PTZControl as PTZControl

class Mqtt(object):
    def __init__(self):
        self.HOST = '47.99.113.188'
        self.PORT = 1883
        self.MSG_SIZE = 128
        self.TIME_INTERVAL = 600
        self.TIME_FORMATE = "%Y-%m-%d-%H-%M"
        self.TOPICALL = 'communication/#'
        self.TOPIC3 = "communication/raspi_to_server"
        self.TOPIC4 = "communication/server_to_raspi"

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
        if msg.topic == self.TOPIC4:
            Control = str(msg.payload, encoding = "utf-8")
            camera = Control.split('_')[0]
            Control_msg = Control.split('_')[1]
            if Control_msg in ['left','right','up','down','capture']:
                if Control_msg == 'left':
                    Flag = PTZControl.pan_tilt_left(camera, 10)
                elif Control_msg == 'right':
                    Flag = PTZControl.pan_tilt_right(camera, 10)
                elif Control_msg == 'up':
                    Flag = PTZControl.pan_tilt_up(camera, 10)
                elif Control_msg == 'down':
                    Flag = PTZControl.pan_tilt_down(camera, 10)
                elif Control_msg == 'capture':
                    Flag = PTZControl.capture_photo(camera, './picture/1.jpg')
                    if Flag == True:
                        self.push_server(client, './picture/1.jpg')
            else:
                Flag = PTZControl.preset_point(int(Control_msg), camera)

            ###########################################
            print('OK')
            ###########################################
            ###########################################
            ###########################################


    def push_server(self, client, msg_dir):
        f = open(msg_dir, 'rb')
        filedata = f.read()
        byteArr = bytes(filedata)
        # client.publish(self.TOPIC3, payload=room, qos=0)
        client.publish(self.TOPIC3, payload=byteArr, qos=0)

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
    # MQTT.push_server(client,'./7301.jpg')

