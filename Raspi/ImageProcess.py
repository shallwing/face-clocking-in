import struct, os, re
import socket as sock



def img_pack(filename:str):
    cwd = os.path.dirname(os.path.abspath(__file__))
    if re.match('panorama', filename):
        fhead = struct.pack(b'128sq', bytes(filename, encoding='utf-8'),
                            os.stat("%s/camera_photo/panorama/%s" % (cwd, filename)).st_size)
    else:

        fhead = struct.pack(b'128sq', bytes(filename, encoding='utf-8'),
                            os.stat("%s/camera_photo/ptz/%s" % (cwd, filename)).st_size)
    # Pack xxx.jpg by 128sq
    return fhead


def img_send(filename:str, fd_sock):\
    cwd = os.path.dirname(os.path.abspath(__file__))
    if re.match('panorama', filename):
        fp = open("%s/camera_photo/panorama/%s" % (cwd, filename), 'rb')
    else:
        fp = open("%s/camera_photo/ptz/%s" % (cwd, filename), 'rb')
    while True:
        data = fp.read(1024)
        if not data:
            break
        else:
            fd_sock.send(data)
