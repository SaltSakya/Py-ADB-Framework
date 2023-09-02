import os
from typing import *

from Utils.device import Device
from Utils.vector import Vector

class ADB:
    # Public
    Log = True

    # Private
    devices = list()
    @staticmethod
    def CMD(cmd):
        if ADB.Log:
            print(os.popen(cmd).read())
        else:
            os.system(cmd)

    @staticmethod
    def Connect(device:Device):
        ADB.CMD(f"adb connect {device.url}")
        ADB.devices.append(device)

    @staticmethod
    def Disconnect(device:Device=None):
        if device:
            for i, dev in enumerate(ADB.devices):
                if dev.url == device.url:
                    ADB.devices.pop(i)
            ADB.CMD(f"adb disconnect {device.url}")

        else:
            ADB.CMD("adb disconnect")
            ADB.devices.clear()
    
    @staticmethod
    def Tap(pos:Vector, device:Device=None):
        if device:
            ADB.CMD(f"adb -s {device.url} shell input tap {pos.x} {pos.y}")
        else:
            ADB.CMD(f"adb shell input tap {pos.x} {pos.y}")




