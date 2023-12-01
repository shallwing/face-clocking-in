
'''
Frames from Aliyun:
(1) Aliyun_send_COUNT_12: "The GPU will receive 12 pictures
(2) Aliyun_send_OK: "ACK signal from Aliyun"

Frames from GPU:
(1) GPU_send_RECV: "The GPU is going to receive pictures
(2) GPU_send_OK: "ACK signal from GPU"
'''


def encode_send(type='ok', count=0):
    frame = "GPU_send_"
    if "ok" == type:
        frame = frame + "OK"
    elif 'recv' == type:
        frame = frame + "RECV"
    else:
        frame = frame + "COUNT_" + str(count)
    return frame


def decode(frame:str):
    if frame.find("OK") >= 0:
        return True
    elif frame.find("COUNT") >= 0:
        count, pos = 0, frame.find("COUNT") + len("COUNT_")
        while pos < len(frame):
            count = count * 10 + int(frame[pos])
            pos += 1
        return count
    elif frame.find("ROOM") >= 0:
        pos = frame.find("ROOM") + len("ROOM_")
        room = frame[pos:]
        return room
    elif frame.find("Roomnums") >= 0:
        count, pos = 0, frame.find("Roomnums") + len("Roomnums_")
        while pos < len(frame):
            count = count * 10 + int(frame[pos])
            pos += 1
        return count
