import struct, os
import socket as sock



def img_get(fd_sock, filename:str, dirname:str, filesize:int, room:str):

    filename = filename.decode().strip('\x00')

    if filename.find('panorama') >= 0:
        if not os.path.exists("./image/%s/panorama/%s" % (room, dirname)):
            os.mkdir("./image/%s/panorama/%s" % (room, dirname))
        new_filename = "./image/%s/panorama/%s/%s" % (room, dirname, filename)
    else:
        if not os.path.exists("./image/%s/ptz/%s" % (room, dirname)):
            os.mkdir("./image/%s/ptz/%s" % (room, dirname))
        new_filename = "./image/%s/ptz/%s/%s" % (room, dirname, filename)

    recvd_size, fp = 0, open(new_filename, 'wb')
    while not recvd_size == filesize:
        if filesize - recvd_size > 1024:
            data = fd_sock.recv(1024)
            recvd_size += len(data)
        else:
            data = fd_sock.recv(filesize-recvd_size)
            recvd_size += len(data)
        fp.write(data)  # Write the image data into picture
    fp.close()
