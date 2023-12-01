import struct
import os, re
import socket as sock


def img_pack(filename:str, dirname:str, room:str):
    if re.match('panorama', filename):
        fhead = struct.pack(b'128sq', bytes(filename, encoding='utf-8'),
                            os.stat("./camera_photo/%s/panorama/%s/%s" % (room, dirname, filename)).st_size)
    else:
        fhead = struct.pack(b'128sq', bytes(filename, encoding='utf-8'),
                            os.stat("./camera_photo/%s/ptz/%s/%s" % (room, dirname, filename)).st_size)
    # Pack xxx.jpg by 128sq
    return fhead


def img_send(filename:str, dirname:str, fd_sock, room:str):
    if re.match('panorama', filename):
        filepath = "./camera_photo/%s/panorama/%s/%s" % (room, dirname, filename)
    else:
        filepath = "./camera_photo/%s/ptz/%s/%s" % (room, dirname, filename)
    fp = open(filepath, 'rb')
    while True:
        data = fp.read(1024)
        if not data:
            break
        fd_sock.send(data)


def img_get(fd_sock, filename, dirname, filesize:int, room:str):
    filename = filename.decode().strip('\x00')

    if filename.find('panorama') >= 0:
        if not os.path.exists("./camera_photo/%s/panorama/%s" % (room, dirname)):
            os.mkdir("./camera_photo/%s/panorama/%s" % (room, dirname))
        new_filename = "./camera_photo/%s/panorama/%s/%s" % (room, dirname, filename)
    else:
        if not os.path.exists("./camera_photo/%s/ptz/%s" % (room, dirname)):
            os.mkdir("./camera_photo/%s/ptz/%s" % (room, dirname))
        new_filename = "./camera_photo/%s/ptz/%s/%s" % (room, dirname, filename)

    recvd_size, fp = 0, open(new_filename, 'wb')
    while not recvd_size == filesize:
        if filesize - recvd_size > 1024:
            data = fd_sock.recv(1024)
            recvd_size += len(data)
        else:
            data = fd_sock.recv(filesize - recvd_size)
            recvd_size += len(data)
        fp.write(data)  # Write the image data into picture
    fp.close()
