import struct, os, re
import socket as sock


def img_pack(filename:str, dirname:str):
    fhead = struct.pack(b'128sq', bytes(filename, encoding='utf-8'),
                        os.stat("/home/lwj/data/picture/%s/%s" % (dirname, filename)).st_size)
    # Pack xxx.jpg by 128sq
    return fhead


def img_send(filename:str, dirname:str, fd_sock):
    filepath = "/home/lwj/data/picture/%s/%s" % (dirname, filename)
    fp = open(filepath, 'rb')
    while True:
        data = fp.read(1024)
        if not data:
            break
        fd_sock.send(data)
