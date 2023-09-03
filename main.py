from ADB.adb import ADB
from Utils.device import Device
from Utils.vector import Vector


mumu = Device()

ADB.KillADB()
ADB.Connect(mumu)
#ADB.ScreenCap().show()