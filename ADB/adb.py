import os
import re
from typing import *
from io import BytesIO
import platform

from Utils.device import Device
from Utils.vector import Vector

from PIL import Image


class ADB:
    # Public
    Log = True

    # Private
    devices = list()

    @staticmethod
    def CMD(cmd, forceLog = False):
        print(cmd)
        if forceLog:
            return os.popen(f"cd ADB && {cmd}")
        if ADB.Log:
            log = os.popen(f"cd ADB && {cmd}").read()
            print(log)
            return log
        else:
            return os.system(f"cd ADB && {cmd}")

    @staticmethod
    def KillADB():
        ADB.CMD("taskkill /f /im adb.exe")

    @staticmethod
    def HEAD(device:Device):
        return (f"-s {device.url}" if device else "")

    @staticmethod
    def Connect(device:Device):
        ADB.CMD(f"adb connect {device.url}")
        size = re.match("^Physical size: (.*?)x(.*?)$", ADB.CMD(f"adb -s {device.url} shell wm size", True).read())
        density = re.match("^Physical density: (.*?)$", ADB.CMD(f"adb -s {device.url} shell wm density", True).read())
        if size and density:
            orientation = int(ADB.CMD("adb shell \"dumpsys input | grep SurfaceOrientation | awk '{print $2}' | head -n 1\"", True).read())
            if orientation%2 == 0:
                device.ScreenParam(size.group(1), size.group(2), density.group(1))
            else:
                device.ScreenParam(size.group(2), size.group(1), density.group(1))
            device.valid = True    
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
    def ScreenCap(device:Device=None):
        if device:
            cmd = f"cd ADB && adb -s {device.url} shell screencap -p"
        else:
            cmd = f"cd ADB && adb shell screencap -p"
        with os.popen(cmd) as w:
            b = w.buffer.read()
            if platform.system() == "Windows":
                b = b.replace(b"\r\n", b"\n")
        im = Image.open(BytesIO(b))            
        return im

    @staticmethod
    def Tap(pos:Vector, device:Device=None):
        ADB.CMD(f"adb {ADB.HEAD(device)} shell input tap {pos.x} {pos.y}")

    @staticmethod
    def Swipe(pos1:Vector, pos2:Vector, duration:float=0.5, device:Device=None):
        ADB.CMD(f"adb {ADB.HEAD(device)} shell input swipe {pos1.x} {pos1.y} {pos2.x} {pos2.y}")  

    @staticmethod
    def Text(text:str, device:Device=None):
        ADB.CMD(f"adb {ADB.HEAD(device)} shell input text {text}")

    @staticmethod
    def KeyEvent(keycode:int, device:Device=None):
        ADB.CMD(f"adb {ADB.HEAD(device)} shell input keyevent {keycode}")

    @staticmethod
    def KeyHome(device:Device=None):
        ADB.KeyEvent(3, device)

    @staticmethod
    def KeyBack(device:Device=None):
        ADB.KeyEvent(4, device)

    @staticmethod
    def KeyMenu(device:Device=None):
        ADB.KeyEvent(82, device)




