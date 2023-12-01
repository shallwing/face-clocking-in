import time
import os
import requests
from requests.auth import HTTPDigestAuth
import cv2 as cv


USER, PASSWD = "admin", "actl9239"


def preset_point(position:int, address:str):
    url = "http://%s/ISAPI/PTZCtrl/channels/1/presets/%d/goto" % (address, position)
    ptz_pre = requests.put(url, auth=HTTPDigestAuth(USER, PASSWD))



def capture_photo(address:str, channel=1, name:str):
    cwd = os.path.dirname(os.path.abspath(__file__))
    capture = cv.VideoCapture("rtsp://%s:%s@%s:554//h264/ch%d/main" %
    (USER, PASSWD, address, channel))
    success, photo = capture.read()
    if success:
        cv.imwrite('%s/camera_photo/panorama/panorama_%s.jpg' % (cwd, name), photo)
    else:
        print("Fail to get the photo from panorama\n")


def pan_tilt_right(address:str, number:int):
    session = requests.Session()
    url = "http://%s/ISAPI/PTZCtrl/channels/1/continuous/" % address
    param1 = "<PTZData><pan>27</pan><tilt>0</tilt></PTZData>"
    param2 = "<PTZData><pan>0</pan><tilt>0</tilt></PTZData>"
    for i in range(number):
        ptz_pre = session.put(url, data=param1, auth=HTTPDigestAuth(USER, PASSWD))
        time.sleep(0.1)
        ptz_pre = session.put(url, data=param2, auth=HTTPDigestAuth(USER, PASSWD))


def pan_tilt_left(address:str, number:int):
    session = requests.Session()
    url = "http://%s/ISAPI/PTZCtrl/channels/1/continuous/" % address
    param1 = "<PTZData><pan>-27</pan><tilt>0</tilt></PTZData>"
    param2 = "<PTZData><pan>0</pan><tilt>0</tilt></PTZData>"
    for i in range(number):
        ptz_pre = session.put(url, data=param1, auth=HTTPDigestAuth(USER, PASSWD))
        time.sleep(0.1)
        ptz_pre = session.put(url, data=param2, auth=HTTPDigestAuth(USER, PASSWD))


def pan_tilt_down(address:str, number:int):
    session = requests.Session()
    url = "http://%s/ISAPI/PTZCtrl/channels/1/continuous/" % address
    param1 = "<PTZData><pan>0</pan><tilt>-27</tilt></PTZData>"
    param2 = "<PTZData><pan>0</pan><tilt>0</tilt></PTZData>"
    for i in range(number):
        ptz_pre = session.put(url, data=param1, auth=HTTPDigestAuth(USER, PASSWD))
        time.sleep(0.2)
        ptz_pre = session.put(url, data=param2, auth=HTTPDigestAuth(USER, PASSWD))


def pan_tilt_up(address:str, number:int):
    session = requests.Session()
    url = "http://%s/ISAPI/PTZCtrl/channels/1/continuous/" % address
    param1 = "<PTZData><pan>0</pan><tilt>27</tilt></PTZData>"
    param2 = "<PTZData><pan>0</pan><tilt>0</tilt></PTZData>"
    for i in range(number):
        ptz_pre = session.put(url, data=param1, auth=HTTPDigestAuth(USER, PASSWD))
        time.sleep(0.2)
        ptz_pre = session.put(url, data=param2, auth=HTTPDigestAuth(USER, PASSWD))
