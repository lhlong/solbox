"""
1. Read tag's code from rfid reader. Check if this code is not exist in our dataset, return
2. Play music
"""
from loguru import logger
import sys
import usb.core
import usb.util
import os
import io
import struct
import time
import zlib
from utils.constants import *
import queue
import threading
from collections import deque
import random

logger.add(os.path.join(LOG_DIR, "app.log"), rotation="1 MB")
tagids = deque(maxlen=20)


def stop_audio():
    while True:
        if (len(tagids) > 0):
            tag_id = tagids.popleft()
            try:
                if tag_id == "0013912333":
                    os.system("killall play")
                    logger.debug("Killall play")
                
            except Exception as e:
                logger.debug(e)
                logger.debug("ERR: Audio stop got a problem")
        else:
            time.sleep(0.001)


def play_audio():
    while True:
        if (len(tagids) > 0):
            tag_id = tagids[-1]
            try:
                tags = [p for p in os.listdir(DATA_DIR)]
                if tag_id in tags:
                    path = os.path.join(DATA_DIR, tag_id)
                    filenames = [p for p in os.listdir(path)]
                    if len(filenames) > 0:
                        idx = random.randrange(len(filenames))
                        path = os.path.join(path, str(filenames[idx]))
                        logger.debug(path)
                        os.system("play -v 3 " + path)
                        tag_id = tagids.popleft()
            except Exception as e:
                logger.debug(e)
                logger.debug("ERR: Audio play got a problem")
        else:
            time.sleep(0.001)


audio_thr = threading.Thread(target=play_audio, args=[])
audio_thr.daemon = True
audio_thr.start()

stop_audio_thr = threading.Thread(target=stop_audio, args=[])
stop_audio_thr.daemon = True
stop_audio_thr.start()

def connect_to_rfid():
    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    time.sleep(0.5)
    if device is None:
        logger.info("RFID device not found.")
        device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        time.sleep(1)
    else:
        if device.is_kernel_driver_active(0):
            try:
                device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                logger.info("Could not detach kernel driver: %s" % str(e))

        try:
            device.set_configuration()
            device.reset()
            logger.info("Just reset RFID device")
            return device[0][(0, 0)][0]

        except usb.core.USBError as e:
            logger.info("Could not set configuration: %s" % str(e))
            pass
        except Exception as e:
            logger.info(e)
            pass


def main():
    # connect to RFID device and set the configuration
    reader = connect_to_rfid()
    data = []

    while True:
        try:
            tt = reader.read(reader.wMaxPacketSize)

            if 30 in tt:
                data += [1]
            elif 31 in tt:
                data += [2]
            elif 32 in tt:
                data += [3]
            elif 33 in tt:
                data += [4]
            elif 34 in tt:
                data += [5]
            elif 35 in tt:
                data += [6]
            elif 36 in tt:
                data += [7]
            elif 37 in tt:
                data += [8]
            elif 38 in tt:
                data += [9]
            elif 39 in tt:
                data += [0]
            elif 40 in tt:
                if len(data) > 10:
                    data = data[:10]
                tag_id = "".join(str(e) for e in data)

                if (len(tagids) == 0) or ((len(tagids) > 0) and (tagids[-1] != tag_id)):
                    tagids.append(tag_id)

                print("TAG ID: {}".format(tag_id))
                tag_id = ""
                data = []

        except usb.core.USBError as e:
            if e.errno == 110:
                data = []
            elif e.errno == 5 or e.errno == 19:
                logger.info(e)
                reader = connect_to_rfid()
            else:
                logger.info("Not known ERROR code")
                logger.info(e)
                reader = connect_to_rfid()
        except Exception as e:
            logger.info(e)
            reader = connect_to_rfid()
            time.sleep(0.5)


if __name__ == "__main__":
    main()
