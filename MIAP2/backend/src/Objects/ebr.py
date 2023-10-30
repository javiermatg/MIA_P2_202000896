import ctypes
import struct
from Utilities.Utilities import coding_str

const = '1s 1s i i i 16s'

    #1s s un string de 1 caracter
    #I es un entero
    #q es un long long
    #16s es un string de 16 caracteres
    #9s es un string de 9 caracteres

class EBR(ctypes.Structure):
    _fields_ = [
        ('status', ctypes.c_char),
        ('fit', ctypes.c_char),
        ('start', ctypes.c_int),
        ('size', ctypes.c_int),
        ('next', ctypes.c_int),
        ('name', ctypes.c_char*16)
    ]
    def __init__(self):
        self.status = b'0'
        self.fit = b'w'
        self.start = -1
        self.size = -1
        self.next = -1
        self.name = b'\0'*16
        
        
    def set_infomation(self, status, fit, start, size, next, name):
        self.status = coding_str(status,1)        
        self.fit = coding_str(fit,1)
        self.start = start
        self.size = size
        self.next = next
        self.name = coding_str(name,16)
        
    
    def display_info(self):
        print(f"status: {self.status.decode()}" )
        print(f"fit: {self.fit.decode()}" )
        print(f"start: {self.start}")
        print(f"size: {self.size}")
        print(f"next: {self.next}")
        print(f"name: {self.name.decode()}")
    def getConst(self):
        return const
    def doSerialize(self):
        serialize = struct.pack(
            const,
            self.status,
            self.fit,
            self.start,
            self.size,
            self.next,
            self.name
        )        
        return serialize 
    def doDeserialize(self, data):
        self.status,self.fit,self.start,self.size,self.next,self.name = struct.unpack(const, data)