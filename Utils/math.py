class Math:
    @staticmethod
    def Clamp(v, l, r):
        if v < l:
            return l
        elif v > r:
            return r
        else:
            return v