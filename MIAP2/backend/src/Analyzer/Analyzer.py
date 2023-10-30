import re
import argparse
import shlex
from Utilities.Utilities import printConsole,printError
from Commands.commands import *

script = False

def commands(data):
    printConsole('===== Terminal ====== ')
    printConsole(" ---- Bienvenido al Sistema de Archivos de  - 202000119 ---- ")
    arr = data

    response = ""
    for command in arr:
      command = re.sub(r"[#][^\n]*", "", command)
      if command == "": continue
      elif re.search("[e|E][x|X][i|I][t|T]", command): break
      response += AnalyzeType(command) + "\n"

    printConsole("... Saliendo del programa ...")
    return response

        

def AnalyzeType(entry):
    try:
        entry = entry.lower()
        printConsole('Analizando comando... ' +  entry)
        #print("Entrey ess: ",entry,'Salto de linea?')
        split_args = shlex.split(entry)
        #print(split_args)
        #print(split_args)
        comando = split_args.pop(0)
        #print(comando)

        if comando == 'mkdisk':
            print('---- Analizando mkdisk... -----')
            return fn_mkdisk(split_args)
            

        elif comando == 'fdisk':
            print('---- Analizando fdisk... -----')
            return fn_fdisk(split_args)
            

        elif comando == 'rmdisk':
            print('---- Analizando rmdisk... -----')
            return fn_rmdisk(split_args)
            

        elif comando == 'mount':
            print('---- Analizando mount... -----')
            return fn_mount(split_args)
               

        elif comando == 'unmount':
            print('---- Analizando unmount... -----')
            return fn_unmount(split_args)
               



        elif comando == 'rep':
            print('---- Analizando rep... -----')
            return fn_rep(split_args)
                

    except Exception as e: pass

def fn_mkdisk(split_args):
    try:
        mkdisk = argparse.ArgumentParser(description='Parametros')
        mkdisk.add_argument('-size',type=int, required= True, help='Especifica el tamaño del disco en mb')
        mkdisk.add_argument('-unit', type=str, default='m', choices=['m','k'],help='Unidades que utilizará el parametro size')
        mkdisk.add_argument('-path', type=str, required=True, help='Ruta donde se creará el archivo que represete al disco')
        mkdisk.add_argument('-fit', default='ff', choices=['bf','ff','wf'])

        args = mkdisk.parse_args(split_args)
        
        if re.search("[.][D|d][s|S][k|K]", args.path) is None: raise Exception('La extensión del archvio debe de ser .dsk')
        print(args)

        
        return c_mkdisk(args.size, args.unit, args.path, args.fit)
        

    except SystemExit:
        printError('Análisis de Argumentos')

    except Exception as e:
        printError(str(e))

def fn_rmdisk(split_args):
    try:
        rmdisk = argparse.ArgumentParser(description='Parametros')
        rmdisk.add_argument('-path', required=True)

        args = rmdisk.parse_args(split_args)

        #if re.search("[.][D|d][s|S][k|K]", args.path) is None: raise Exception('La extensión del archvio debe de ser .dsk')
        return c_rmdisk(args)
    except SystemExit:
        printError('Análisis de Argumentos')
    
    except Exception as e:
        printError(str(e))            

def fn_fdisk(split_args):

    delete = False
    add = False
    for command in split_args:
        if re.search("[-][a][d][d]", command):
            add = True
        if re.search("[-][d][e][l][e][t][e]", command):
            delete = True
    #print(delete,add)
    try:
        fdisk = argparse.ArgumentParser(description='Parametros')
        fdisk.add_argument('-size',type=int, required= True, help='Especifica el tamaño del disco en mb')        
        fdisk.add_argument('-unit', type=str, default='k', choices=['b','m','k'],help='Unidades que utilizará el parametro size')
        fdisk.add_argument('-path', type=str, required=True, help='Ruta donde se creará el archivo que represete al disco')
        fdisk.add_argument('-name', type=str, required=True, help='Ruta donde se creará el archivo que represete al disco')
        fdisk.add_argument('-type', default='p', choices=['p','e','l'], help='Indica el tipo de partición')
        fdisk.add_argument('-fit', default= 'wf', choices=['bf','ff','wf'], help='Indica el ajuste que utilizará la partición')
        fdisk.add_argument('-delete', default='full', choices=['full'], help='Eliminación de una partición')
        fdisk.add_argument('-add', type=int, help='Agregar o eliminar espacio de la partición')
        
        args = fdisk.parse_args(split_args)
        if (args.size > 0) is None: raise Exception('El tamaño debe ser positivo y mayor a cero')
        
        if re.search("[.][D|d][s|S][k|K]", args.path) is None: raise Exception('La extensión del archvio debe de ser .dsk')

        return c_fdisk(args,add,delete)
        #print(args.add)
    except SystemExit:
        printError('Análisis de Argumentos')

    except Exception as e:
        printError(str(e))

def fn_mount(split_args):
    try:
        mount = argparse.ArgumentParser(description='Parametros')
        mount.add_argument('-name', type=str, required=True)
        mount.add_argument('-path', type =str, required=True)

        args = mount.parse_args(split_args)

        return c_mount(args)
    
    except SystemExit:
        printError('Análisis de Argumentos')
    except Exception as e:
        printError(str(e))  

def fn_unmount(split_args):
    try:
        unmount = argparse.ArgumentParser(description='Parametros')
        unmount.add_argument('-id', required=True)

        args = unmount.parse_args(split_args)
        return c_unmount(args)
    except SystemExit:
        printError('Análisis de Argumentos')
    except  Exception as e:
        printError(str(e))    

def fn_rep(split_args):
    try:
        rep = argparse.ArgumentParser(description='Parametros')
        rep.add_argument('-id', type=str, required=True)
        rep.add_argument('-path', type =str, required=True)
        rep.add_argument('-name', type=str, required=True, choices=['mbr','disk','inode','journaling','block','mb_inode','bm_block','tree','sb','file','ls'])
        rep.add_argument('-ruta', type=str)
        args = rep.parse_args(split_args)
        return c_rep(args)
    except SystemExit:
        printError('Análisis de Argumentos')
    except Exception as e:
        printError(str(e))    

def fn_mkfs(split_args):
    try:
        mkfs = argparse.ArgumentParser(description='Parametros')
        mkfs.add_argument('-id', required=True)
        mkfs.add_argument('-type', default='full')
        mkfs.add_argument('-fs', default='2fs', choices=['2fs', '3fs'])

        args = mkfs.parse_args(split_args)
        #c_mkfs(args)
    except SystemExit:
        printError('Análisis de Argumentos')
    except  Exception as e:
        printError(str(e))    



