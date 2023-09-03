from ADB.adb import Device
from Utils.math import Math

class Vector:
    def __init__(self, x, y, device:Device=None):
        if device:
            self.x = Math.Clamp(x, 0, 1) * device.width
            self.y = Math.Clamp(y, 0, 1) * device.height
        else:
            self.x = x
            self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __div__(self, other):
        return Vector(self.x / other, self.y / other)