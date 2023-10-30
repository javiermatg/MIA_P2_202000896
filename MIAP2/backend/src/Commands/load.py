import pickle
import ctypes
from Utilities.Utilities import*


def Fwrite_displacement(file, displacement, obj):
    #print("Writing in: ", displacement)
    #print("Size data: ",  len(data))
    data = obj.doSerialize()
    
    file.seek(displacement)
    file.write(data)

def Fread_displacement(file, displacement,obj):
    try:
        #print("Reading in: ", displacement)
        file.seek(displacement)
        data = file.read(len(obj.doSerialize()))
        #print("Size data: ",  len(data))
        obj.doDeserialize(data)
    except Exception as e:
        printError(f"Error reading object err: {e}")
    
def Fcreate_file(file_name):
    try:
        fileOpen = open(file_name, "wb") 
        fileOpen.close()  
        printSuccess("=====File created successfully!======")
        return False
    except Exception as e:
        printError(f"Error creating the file: {e}")
        return True

def Winit_size(file,size, unit):
    #mb to bytes -> mb * 1024kb/1mb * 1024b/1kb -> mb * 1024 * 1024

    buffer = b'\0'
    if unit == 'k':
        times_to_write = size * 1024
    elif unit == 'm':
        times_to_write =  size  * 1024 * 1024

    #print(f"Expected File Size: {len(buffer)*times_to_write} bytes")
    
    for i in range(times_to_write):
        file.write(buffer)
    
    print("=====Size apply successfully!======")



  