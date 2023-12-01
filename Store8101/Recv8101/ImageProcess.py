import struct
import os, re
import socket as sock


def img_pack(filename:str, dirname:str):
    fhead = struct.pack(b'128sq', bytes(filename, encoding='utf-8'),
                        os.stat("./camera_photo/%s/%s" % (dirname, filename)).st_size)
    # Pack xxx.jpg by 128sq
    return fhead


def img_get(fd_sock, filename, dirname, filesize:int):
    filename = filename.decode().strip('\x00')
    if not os.path.exists("./camera_photo/%s" % dirname):
        os.mkdir("./camera_photo/%s" % dirname)
    new_filename = "./camera_photo/%s/%s" % (dirname, filename)

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