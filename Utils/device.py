
class Device:
    def __init__(self, host="127.0.0.1", port="16384"):
        self.url = f"{host}:{port}"
        self.size = (self.width, self.height) = (1280, 720)
        self.dpi = 180