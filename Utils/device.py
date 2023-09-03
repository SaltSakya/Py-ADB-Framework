
class Device:
    def __init__(self, host="127.0.0.1", port="16384"):
        self.url = f"{host}:{port}"
        self.size = (self.width, self.height) = (1280, 720)
        self.dpi = 180
        self.valid = False
    
    def ScreenParam(self, width:int, height:int, dpi:int):
        self.size = self.width, self.height = int(width), int(height)
        self.dpi = int(dpi)

    def RotateToVertical(self):
        self.size = (self.width, self.height) = (min(self.width, self.height), max(self.width, self.height))

    def RotateToHorizontal(self):
        self.size = (self.width, self.height) = (max(self.width, self.height), min(self.width, self.height))