
'''
Frames from Aliyun:
(1) Aliyun_send_COUNT_12: "The GPU will receive 12 pictures
(2) Aliyun_send_OK: "ACK signal from Aliyun"

Frames from Raspi:
(1) Pi_send_COUNT_12: "The Raspi is going to send 12 pictures
(2) Pi_send_OK: "ACK signal from Pi"
'''
import re


def encode_send(count=0, type='ok', room=""):
    frame = "Pi_send_"
    if 'ok' == type:
        frame = frame + 'OK'
    elif 'count' == type:
        frame = frame + 'COUNT_' + str(count)
    elif 'room' == type:
        frame = frame + 'room_' + room
    return frame


def decode(frame:str):
    if frame.find("OK") >= 0:
        return True
    else:
        return False
