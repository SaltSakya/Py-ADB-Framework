
from time import time, sleep
from threading import Thread

from ADB.adb import ADB
from Utils.device import Device

RUNNING = True

def CapLoop():
    t = time()
    while RUNNING:
        ADB.CMD(f"adb exec-out screencap -p > ../Resources/screencaps/{int(t)}.png")
        t_ = time()
        sleep(max(3 - t_ + t, 0))
        t = t_

    print("Stop running!")


if __name__ == "__main__":
    ADB.Connect(Device())

    Thread(target=CapLoop).start()
    
    