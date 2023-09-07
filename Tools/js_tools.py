import numpy as np

class Number:
    def __init__(self, n):
        self.n = np.int64(n)

    def __repr__(self):
        return str(self.n)
    
    def __add__(self, a):
        if type(a) == Number:
            return Number(self.n + a.n)
        else:
            return Number(self.n + a)
    
    def __sub__(self, a):
        if type(a) == Number:
            return Number(self.n - a.n)
        else:
            return Number(self.n - a)
        
    def __rsub__(self, a):
        if type(a) == Number:
            return Number(a.n - self.n)
        else:
            return Number(a - self.n)
    
    def __mul__(self, a):
        if type(a) == Number:
            return Number(self.n * a.n)
        else:
            return Number(self.n * a)
    
    def __truediv__(self, a):
        if type(a) == Number:
            return Number(self.n / a.n)
        else:
            return Number(self.n / a)
        
    def __mod__(self, a):
        if type(a) == Number:
            return Number(self.n % a.n)
        else:
            return Number(self.n % a)
        
    def __and__(self, a):
        n = self.n.astype(np.int32)
        if type(a) == Number:
            a = a.n.astype(np.int32)
        else:
            a = np.int64(a).astype(np.int32)
        return Number(n & a)
        
    def __or__(self, a):
        n = self.n.astype(np.int32)
        if type(a) == Number:
            a = a.n.astype(np.int32)
        else:
            a = np.int64(a).astype(np.int32)
        return Number(n | a)
        
    def __xor__(self, a):
        n = self.n.astype(np.int32)
        if type(a) == Number:
            a = a.n.astype(np.int32)
        else:
            a = np.int64(a).astype(np.int32)
        return Number(n ^ a)
        
    def __invert__(self):
            n = self.n.astype(np.int32)
            return Number(~n)

    def __lshift__(self, a):
        n = self.n.astype(np.int32)
        if type(a) == Number:
            a = a.n.astype(np.int32)
        else:
            a = np.int64(a).astype(np.int32)
        return Number(n << a)
        
    def __rshift__(self, a):
        n = self.n.astype(np.uint32)
        if type(a) == Number:
            a = a.n.astype(np.int32)
        else:
            a = np.int64(a).astype(np.int32)
        a %= 32
        if a == 0:
            return Number(n)
        return Number(int("0"*a + np.binary_repr(n, 32)[:-a], base=2))