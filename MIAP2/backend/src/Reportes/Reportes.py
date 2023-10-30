from graphviz import Digraph
import graphviz
from Utilities.Utilities import *


def r_disk(label, path):
    

    encabezado = """
            
    
    subgraph cluster_0 {
        bgcolor="#68d9e2"
        node [style="rounded" style=filled];

            """
    node = 'node_A [shape=record label="' + label+'"];'
    fin = "} "
    dii = """   
        subgraph cluster_0 {
        bgcolor="#68d9e2"
        node [style="rounded" style=filled];
       
        node_A [shape=record    label="MBR|Libre|P1|{Extendida|{EBR|LOGICA|EBR|LOGICA}}|PArticion"];
    }
            """
    todo = encabezado + node + fin
    #body += encabezado
    g = Digraph(name='Disk',format='jpg',body= todo)
    #print(g)
    #g.subgraph(name='Cluster_0',body='node_A [shape=record    label="MBR|Libre|{Extendida|{EBR|LOGICA|EBR|LOGICA}}|PArticion"];')
    
   
    #print(g.source)
    g.render(path, view=False)
    
    """g.attr('node', style="rounded")
    g.attr('node',  style="filled")
    
    g.attr(bgcolor = "#68d9e2")
    
    
    g.node(label=label, name='node_A', shape='record')"""

def r_mbr(mbr_object, path, logicasL):

    testeo = """fontname="Helvetica,Arial,sans-serif"
        node [ shape=none fontname=Helvetica ]
        n3 [ label = <
        <table border="1">
        <tr><td colspan="2" bgcolor="dodgerblue4">REPORTE MBR</td></tr>
        <tr><td bgcolor="white">mbr_tamano</td><td bgcolor="white">{mbr_object.size} </td></tr>
        <tr><td bgcolor="dodgerblue1">mbr_fecha_cracion</td><td bgcolor="dodgerblue1">{mbr_object.date_creation.decode()}</td></tr>
        <tr><td bgcolor="white">mbr_disk_signature</td><td bgcolor="white">{mbr_object.asignature}</td></tr>

        <tr><td colspan="2" bgcolor="dodgerblue4">"</td></tr>
        <tr><td bgcolor="white">mbr_tamano</td><td bgcolor="white">two </td></tr>
        <tr><td bgcolor="dodgerblue1">mbr_fecha_cracion</td><td bgcolor="dodgerblue1">four</td></tr>
        <tr><td bgcolor="white">mbr_disk_signature</td><td bgcolor="white">two </td></tr>
        <tr><td bgcolor="white">mbr_tamano</td><td bgcolor="white">two </td></tr>
        <tr><td bgcolor="dodgerblue1">mbr_fecha_cracion</td><td bgcolor="dodgerblue1">four</td></tr>
        <tr><td bgcolor="white">mbr_disk_signature</td><td bgcolor="white">two </td></tr>

        </table>>]"""
    try:
        encabezado = f"""
        fontname="Helvetica,Arial,sans-serif"
        node [ shape=none fontname=Helvetica ]
        n3 [ label = <
        <table border="1">
        <tr><td colspan="2" bgcolor="dodgerblue4">REPORTE MBR</td></tr>
        <tr><td bgcolor="white">mbr_tamano</td><td bgcolor="white">{mbr_object.size} </td></tr>
        <tr><td bgcolor="dodgerblue1">mbr_fecha_cracion</td><td bgcolor="dodgerblue1">{mbr_object.date_creation.decode()}</td></tr>
        <tr><td bgcolor="white">mbr_disk_signature</td><td bgcolor="white">{mbr_object.asignature}</td></tr>
        """
        partitions = ''
        for partition in mbr_object.partitions:
            if partition.status.decode() == '1' and partition.type.decode() != 'l':
                partitions += f""" <tr><td colspan="2" bgcolor="dodgerblue4">Partition {partition.type.decode()}</td></tr>
                <tr><td bgcolor="white">part_status</td><td bgcolor="white">{partition.status.decode()}</td></tr>
                <tr><td bgcolor="dodgerblue1">part_type</td><td bgcolor="dodgerblue1">{partition.type.decode()}</td></tr>
                <tr><td bgcolor="white">part_fit</td><td bgcolor="white">{partition.fit.decode()}</td></tr>
                <tr><td bgcolor="white">part_start</td><td bgcolor="white">{partition.start}</td></tr>
                <tr><td bgcolor="dodgerblue1">part_size</td><td bgcolor="dodgerblue1">{partition.size}</td></tr>
                <tr><td bgcolor="white">part_name</td><td bgcolor="white">{partition.name.decode()}</td></tr>
                                                                                                """

        for partition in logicasL:
            partitions += f""" <tr><td colspan="2" bgcolor="dodgerblue4">Partition Logica</td></tr>
                <tr><td bgcolor="white">part_status</td><td bgcolor="white">{partition.status.decode()}</td></tr>
                <tr><td bgcolor="dodgerblue1">part_next</td><td bgcolor="dodgerblue1">{partition.next}</td></tr>
                <tr><td bgcolor="white">part_fit</td><td bgcolor="white">{partition.fit.decode()}</td></tr>
                <tr><td bgcolor="white">part_start</td><td bgcolor="white">{partition.start}</td></tr>
                <tr><td bgcolor="dodgerblue1">part_size</td><td bgcolor="dodgerblue1">{partition.size}</td></tr>
                <tr><td bgcolor="white">part_name</td><td bgcolor="white">{partition.name.decode()}</td></tr>
                                                                                                """
        completo = encabezado + partitions + '</table>>]'
    
        g = Digraph(name='MBR', format='jpg',body=completo)
        g.render(path, view=False)
    except Exception as e:
        printError(f'Error al crear el reporte: {e}')

    try: #REPORTE EBR
        encabezadoE = f"""
        fontname="Helvetica,Arial,sans-serif"
        node [ shape=none fontname=Helvetica ]
        n3 [ label = <
        <table border="1">
        <tr><td colspan="2" bgcolor="dodgerblue4">REPORTE EBR</td></tr>
        """
    
        partitionsE = ''
        for partition in logicasL:
            partitionsE += f""" <tr><td colspan="2" bgcolor="dodgerblue4">Partition Logica</td></tr>
                <tr><td bgcolor="white">part_status</td><td bgcolor="white">{partition.status.decode()}</td></tr>
                <tr><td bgcolor="dodgerblue1">part_next</td><td bgcolor="dodgerblue1">{partition.next}</td></tr>
                <tr><td bgcolor="white">part_fit</td><td bgcolor="white">{partition.fit.decode()}</td></tr>
                <tr><td bgcolor="white">part_start</td><td bgcolor="white">{partition.start}</td></tr>
                <tr><td bgcolor="dodgerblue1">part_size</td><td bgcolor="dodgerblue1">{partition.size}</td></tr>
                <tr><td bgcolor="white">part_name</td><td bgcolor="white">{partition.name.decode()}</td></tr>
                                                                                                """
        completoE = encabezadoE + partitionsE + '</table>>]'
    
        e = Digraph(name='EBR', format='jpg',body=completoE)
        e.render(path+'E', view=False)
    except Exception as e:
        printError(f'Error al crear el reporte: {e}')    
    