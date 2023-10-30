import subprocess
import os
from Objects.mbr import MBR
from Objects.partition import Partition
from Objects.ebr import EBR
from .load import *
from Reportes.Reportes import *
from Global.Global import *
from Objects.logicas import Logicas

#logicas = []

def c_mkdisk(size, unit, path, fit):

    n_path = path.replace(" ","")
    #print("nuevo path",n_path)
    folder_path = os.path.dirname(n_path)
    subprocess.run(f"mkdir -p {folder_path}", shell=True)
    
    if (Fcreate_file(n_path)): return

    try:                                #Iniciar el archivo con \0 y escribir el objeto MBR al inicio
        fileOpen = open(n_path, "rb+") 
        Winit_size(fileOpen,size, unit)
        displacement = 0
        mbr_object = MBR()
        mbr_object.set_infomation(get_sizeB(size,unit),fit)
        #mbr_object.display_info()
        Fwrite_displacement(fileOpen,displacement,mbr_object)
        
        fileOpen.close()  
        #print('==== Se escribió el MBR correctamente')
        printSuccess('===== Se creó el disco de manera correcta=====')
        return "===== Se creó el disco de manera correcta====="
    except Exception as e:
          print(f"Error Writing the file: {e}") 

def c_rmdisk(args):

    
    path = args.path.replace(" ","")
    try:
        subprocess.run(f"rm {path}", shell=True)
        #printSuccess('Disco eliminado de manera correcta')
        return 'Disco eliminado de manera correcta'
    except Exception as e:
       #printError('No es posible eliminar el disco: '+e) 
        return 'No es posible eliminar el disco: '+e

def c_fdisk(args, add, delete):
    #print("args: ", args)
    #disk = [['name', 2, 300],[0],[1,'new_name', 2, 200],[100],['name', 2, 300],[0],['name', 2, 300],[0]]


    
    
    path = args.path.replace(" ","")
    mbr_object = MBR()
    new_size = get_sizeB(args.size,args.unit)
    try:
        fileOpen = open(path, "rb+")
    except Exception as e:
        printError(str(e))  
        return "Error, NO se encontró el directorio"  
    Fread_displacement(fileOpen,0,mbr_object)

    """if delete: #Eliminar una partición del disco
        for i in range(0, len(mbr_object.partitions)):
            if mbr_object.partitions[i].name.decode() == args.name:
                #printSuccess('Se eliminó: '+ mbr_object.partitions.pop(i).name.decode() +' de manera correcta')
                
                new_partition = Partition()
                new_partition.set_infomation('0','p','w',mbr_object.partitions[i].start, mbr_object.partitions[i].size,'')
                mbr_object.partitions[i] = new_partition
                Fwrite_displacement(fileOpen,0,mbr_object)
                fileOpen.close()
                printSuccess('Se eliminó la partición correctamente')
                return
        

        for logica in logicas:
            if logica.asignature == mbr_object.asignature:
                for log in logica.logicas:
                    if log.name.decode() == args.name:
                        log.status = '0'
                        log.name = ''
                        return printSuccess('Partición lógica eliminada correctamente')
        
        return printError(f'No se encontró la partición {args.name} en el disco')    """        
        
    """if add:
        validacion = 0
        for partition in mbr_object.partitions:
            if partition.name.decode() == args.name:
                if int(args.add) < 0:
                    validacion = partition.size - int(args.add)
                    if validacion > 0:
                        partition.size = validacion
                        return printSuccess('Se quitó el tamaño de manera correcta')
                    return printError('Espacion insuficiente para eliminar')
                else:
                    
                    partition.size = partition.size + int(args.add)
                    return printSuccess('Espacio agregado correctamente')
    """
    extendida = True
    logica = False
    for partition in mbr_object.partitions: #Validación de partición extendida y lógica
        if partition.type.decode() == 'e' and args.type == 'e':
            extendida = False                     
            break

        if partition.type.decode() == 'e' and args.type == 'l':
            logica = True
          
    if extendida is False:
        #printError('No puede haber más de una partición extendida')
        fileOpen.close()
        return 'No puede haber más de una partición extendida'
        
        
    
    if args.type == 'l' and logica is False:
        #printError('No se puede crear una partición lógica si aún no existe una extendida')
        fileOpen.close()
        return 'No se puede crear una partición lógica si aún no existe una extendida'
        



    
    if args.size is not None: # creting partition
        start = len(MBR().doSerialize())
        index = 0
        #new_name = args.name
        #n_copia = 0
        if args.type == 'l':
            obj_logicas = Logicas()
            obj_logicas.set_infomation(mbr_object.asignature)
           
            log = []
            indice = 0
            for logica in logicas:
                if logica.asignature == mbr_object.asignature:
                    log = logica.logicas
                    break
                indice += 1

            start_e = len(EBR().doSerialize())
            displacement = 0
            next_e = 0
            total_e = 0
            disponible_e = 0
            for partition in mbr_object.partitions:
                if partition.type.decode() == 'e':
                    displacement = partition.start
                    start_e += partition.start
                    total_e = partition.start + partition.size
            ebr_object = EBR()
            disponible_e = (total_e - len(EBR().doSerialize()) )
            if len(log) == 0 and args.size < disponible_e:
                next_e = start_e + new_size   
                     
                ebr_object.set_infomation('1', args.fit,start_e,new_size,next_e,args.name)
                Fwrite_displacement(fileOpen,displacement, ebr_object) 
                fileOpen.close()
                
                log.append(ebr_object)
                obj_logicas.logicas = log
                #print("0:" ,indice)
                logicas.append(obj_logicas)
               #printSuccess('Se agregró la partición lógica correctamente')
                
                #print(logicas)
                return 'Se agregró la partición lógica correctamente'

            else:
                for partitionl in log:
                    if partitionl.size != -1:
                        start_e = partitionl.next
                        displacement = partitionl.next
                    else:
                        break
                
                next_e = start_e + new_size
                #print(next_e)
                #print(total_e-len(EBR().doSerialize()))
                #print(new_size)
                if next_e < (total_e-len(EBR().doSerialize())) and len(log)<16:
                    ebr_object.set_infomation('1', args.fit,start_e,new_size,next_e,args.name)
                    Fwrite_displacement(fileOpen,displacement, ebr_object) 
                    fileOpen.close()
                    log.append(ebr_object)
                    obj_logicas.logicas = log
                    #print("mas d 0 :",indice)
                    logicas[indice] == obj_logicas
                    #logicas.append(mbr_object.asignature,ebr_object)
                    #printSuccess('Se agregró la partición lógica correctamente')
                    #print(logicas)
                    return 'Se agregró la partición lógica correctamente'
                else:
                    #printError('Espacio insuficiente, No se puedo agregar la partición lógica')
                    """print(logicas)
                    for log in logicas:
                        print('logicaObj: ',log.logicas)
                    """
                    return 'Espacio insuficiente, No se puedo agregar la partición lógica'
        else:
                
            for partition in mbr_object.partitions:
                if partition.size != -1:
                    if partition.name.decode() == args.name:
                        #return printError(f'La partición {args.name} ya existe en el sistema')
                        return f'La partición {args.name} ya existe en el sistema'
                    if partition.status.decode() == '1':
                        start = partition.start + partition.size
                        index += 1
                    elif partition.status.decode() == '0':
                        if args.size < partition.size:
                            index += 1    
                    
                    #n_copia += 1
                    
                    #new_name = args.name + 'copia' + str(n_copia)
                    #print(new_name)
                else:
                    break
        
        
        if index < 4:
            disponible = (mbr_object.size - (start ))
            #print(mbr_object.size)
            #print(start)
            #print('Espacio disponible: ', disponible)
            if new_size > (disponible):
                printError('Tamaño insuficiente en el Disco local para crear la partición')    
                fileOpen.close()
                return 'Error, Tamaño insuficiente en el Disco local para crear la partición'
            new_partition = Partition()
            new_partition.set_infomation('1',args.type,args.fit,start,new_size,args.name)
            mbr_object.partitions[index] = new_partition
            Fwrite_displacement(fileOpen,0,mbr_object)
            #printSuccess('Se agregó la partición de manera correcta')
            return 'Se agregó la partición de manera correcta'

            
                
        else:
            #printError(f'No se pudo crear la partición: {args.name}. Se llegó al límite de particiones(4)')   
            return  f'No se pudo crear la partición: {args.name}. Se llegó al límite de particiones(4)'
        
    #mbr_object.partitions[0].get_infomation()    
    #mbr_object.partitions[1].get_infomation()
    #mbr_object.partitions[2].get_infomation()
    #mbr_object.partitions[3].get_infomation()

   
    fileOpen.close()

def c_rep(args):
    #print('Logicas: ', logicas)
    #path = args.path.replace(" ","") temp = [id,crr_partition ,args.path]
    path = ''
    for mounted in mounted_partitions:
        if mounted[0] == args.id:
            path = mounted[-1]
            break
    
    if path == '':
        # printError('No hay coincidencias con el ID: ' + args.id)
        return 'No hay coincidencias con el ID: ' + args.id
    
    if args.name == 'disk':
        try:
            fileOpen = open(path, 'rb+')
            mbr_object = MBR()
            Fread_displacement(fileOpen, 0, mbr_object)
            logicasL = []
            for logica in logicas:
                if logica.asignature == mbr_object.asignature:
                    logicasL = logica.logicas
                    
            libre = mbr_object.size - (mbr_object.partitions[3].start + mbr_object.partitions[3].size)
            ocupado = 0
            node_p = ''
            p_zise = 0
            for partition in mbr_object.partitions:
                if partition.status.decode() == '1':
                    if partition.type.decode() == 'e':
                        libre = 0
                        p_size = (partition.size*100)/mbr_object.size
                        node_p += '|{'+ partition.name.decode()+ str(p_size)+'%|{EBR' 
                        if len(logicasL) > 0:
                            
                            for log in logicasL:
                                p_size = (log.size* 100)/partition.size
                                if log.status.decode() == 0 and log.size != -1:
                                    node_p += f"|Libre \n {p_size}%"
                                else:
                                    node_p += f"|EBR |{log.name.decode()} \n {p_size}%"
                                libre = (partition.start + partition.size) - log.next

                            if libre > 0:
                                p_size = round((libre*100)/partition.size)
                                node_p += f"|Libre \n {p_size}%"
                         
                        node_p += '} }'
                        ocupado = partition.start + partition.size
                    else:
                        p_size = (partition.size * 100)/mbr_object.size
                        node_p += f"|{partition.name.decode()} \n {p_size}%" 
                        ocupado = partition.start + partition.size
                elif partition.status.decode() == '0' and partition.size != -1:
                        p_size = (partition.size * 100)/mbr_object.size
                        node_p += f"|Libre \n {p_size}%"
            
                    
                    
            node_i = 'MBR'
            node_temp = (((mbr_object.size - ocupado)*100)/mbr_object.size)
            node_d = round(node_temp,3)
            node = node_i + node_p + f"|Libre \n {node_d} %"
            #node = ' MBR|Libre|{Extendida|{EBR|LOGICA|EBR|LOGICA}}|PArticion'
            r_disk(node, args.path)
            #printSuccess('Reporte Generado')
            fileOpen.close()
            return 'Reporte Generado correctamente'
        except Exception as e:
            #printError(f"Error leyendo el archivo: {e}") 
            return f"Error leyendo el archivo: {e}"

    elif args.name == 'mbr':

        try:
            fileOpen = open(path, 'rb+')
            mbr_object = MBR()
            Fread_displacement(fileOpen,0, mbr_object)
            logicasL = []
            for logica in logicas:
                if logica.asignature == mbr_object.asignature:
                    logicasL = logica.logicas
                    break
             
            r_mbr(mbr_object, args.path, logicasL)
            #printSuccess('Reporte Generado')
            return 'Reporte Generado'
        except Exception as e:
            #printError(f"Error leyendo el archivo: {e}")
            return f"Error leyendo el archivo: {e}"

def c_mount(args):

 
    #print("args: ", args)
    path = args.path.replace(" ","")
    if len(mounted_partitions) > 0:
        for mounted in mounted_partitions:
            if mounted[1].name.decode() == args.name:
                #return printWarning(f'La partición {args.name} ya fue montada')
                return f'La partición {args.name} ya fue montada'
    try:
        crr_mbr = MBR()
        Crrfile = open(path, "rb+")
        Fread_displacement(Crrfile,0,crr_mbr)
        
        crr_partition = Partition()
        crr_partitionl = EBR()
        #print(crr_mbr.partitions)
        for partition in crr_mbr.partitions:
            #print('El nombre es',partition.name.decode())
            #print('El tamaño es es',partition.size)
            if partition.size != -1: #pendiente de modificar por los delete o eliminar partición
                
                if partition.name.decode() == args.name:
                    #printError('3')
                    if partition.type.decode() == 'e':
                        #printError('4')
                        #return printError("NO se puede montar una partición extendida")
                        return "NO se puede montar una partición extendida"
                    crr_partition = partition

        for logica in logicas:
            if logica.asignature == crr_mbr.asignature:
                for log in logica.logicas:
                    printError('1')
                    if log.name.decode() == args.name:
                        crr_partitionl = log
                        break

        if crr_partition.name.decode() == args.name or crr_partitionl.name.decode() == args.name:
            pass

        else:
            #return printError(f" La partición {args.name} no existe en el sistema")        
            return f" La partición {args.name} no existe en el sistema"
        
            # F = XX +  NUM PARTITION + NOMBRE DISCO donde XX es el numero de carnet

        nombre_archivo = os.path.splitext(os.path.basename(path))[0]
        index = 1
        for data in mounted_partitions:
            if data[2] == path:
                index = int(data[0][2:3]) + 1
        id = "96" + str(index) + nombre_archivo
        print("id:",id)
        if crr_partition.size != -1:
            temp = [id,crr_partition ,path]
            #printWarning("Entro a partition")
        else:
            temp = [id,crr_partitionl ,path]
            #printWarning("Entro a partitionL")

        mounted_partitions.append(temp)
        #print(mounted_partitions)
        #printSuccess('Partición montadda correctamente')
        return 'Partición montadda correctamente'
        
        Crrfile.close()
    except Exception as e:
        #printError(f'Error leyendo el archivo {e}')    
        return 'Error leyendo el archivo {e}'

def c_unmount(args):
    for partition in mounted_partitions:
        if partition[0] == args.id:
            mounted_partitions.remove(partition)
            
            #print(mounted_partitions)
            #return printSuccess(f"Se demsmontó la partición {args.id} correctamente")
            return f"Se demsmontó la partición {args.id} correctamente"
        
    #printError('No exite la partición en el sistema')  
    return 'No exite la partición en el sistema'

def c_mkfs():
    print('hola munñdo')