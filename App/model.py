"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
import math as mt
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    
    data_structs = {"comparendos": None, # Grafo: peso numéro de comparendos
                    "ditsancias": None, # Grafo: peso distancia
                    "mapa_vertices": None, 
                    
                    "mapa_vehiculos_maxpq_comparendos": None, # Mapa: {llave: vehiculo, valor: max_pq_comparendos}
                    "mapa_vehiculos": None, # Mapa: {llave: vehiculo, valor: mapa_vertices_vehiculo}
                    
                    "mapa_gravedad_maxpq_comparendos": None, # Mapa: {llave: gravedad, valor: max_pq_comparendos}
                    "mapa_gravedad_comparendos": None, #Mapa: {llave: gravedad, valor: lista_comparendos}
                    
                    "mapa_localidades": None, # Mapa: {llave: localidad, valor: lista_comparendos}
                    
        
                    }
    
    
    data_structs["comparendos"] = gr.newGraph(datastructure="ADJ_LIST", directed=False)
    
    data_structs["distancias"] = gr.newGraph(datastructure="ADJ_LIST", directed=False)
    
    data_structs["mapa_vertices"] = mp.newMap(numelements=228045, maptype="PROBING", loadfactor=0.5)
    
    data_structs["mapa_vehiculos_maxpq_comparendos"] = mp.newMap(numelements=35, maptype="PROBING", loadfactor=0.5)
    
    data_structs["mapa_vehiculos"] = mp.newMap(numelements=35, maptype="PROBING", loadfactor=0.5)
    
    data_structs["mapa_gravedad_comparendos"] = om.newMap(omaptype="RBT", cmpfunction=compare_gravedad)
    
    data_structs["mapa_gravedad_maxpq_comparendos"] = mp.newMap(numelements=115, maptype="PROBING", loadfactor=0.5)
    
    data_structs["mapa_localidades"] = mp.newMap(numelements=20, maptype="PROBING", loadfactor=0.5)
    
    data_structs["mapa_localidades_maxpq_comparendos"] = mp.newMap(numelements=20, maptype="PROBING", loadfactor=0.5)
    
    return data_structs
    


# Funciones para agregar informacion al modelo

def add_data(data_structs, archivo, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    mapa_vertices = data_structs["mapa_vertices"] # Mapa: {lllaeve: id_vertice, valor: vertice}
    mapa_vehiculos = data_structs["mapa_vehiculos"] # Mapa: {llave: vehiculo, valor: mapa_vertices_vehiculo}
    mapa_gravedad_comparendos = data_structs["mapa_gravedad_comparendos"] # Mapa: {llave: gravedad, valor: lista_comparendos}
    mapa_localidades = data_structs["mapa_localidades"] # Mapa: {llave: localidad, valor: lista_comparendos}
    
    match archivo:
        case "bogota_vertices.txt": # Se agrega un vertice al mapa de vertices
            data = data.split(',') # Se formatea la información de string "# # #" a lista ["#", "#", "#"]
            id = data[0] # Se obtiene el identificador del vertice en la primera posición de la lista
            longitud = float(data[1]) # Se obtiene la longitud del vertice en la segunda posición de la lista
            latitud = float(data[2]) # Se obtiene la latitud del vertice en la tercera posición de la lista
            
            
            # Se crea un vertice con la información obtenida en formato dict
            vertice = {"id": id, # Identificador del vertice
                        "long": longitud, # Longitud del vertice
                       "lat": latitud, # Latitud del vertice
                       "estaciones": lt.newList("ARRAY_LIST"), # Lista de estaciones de policia más cercanas al vertice. Una si es única, varias si hay empate
                       "comparendos": lt.newList("ARRAY_LIST"), # Lista de comparendos en el vertice
                       }
            
            
            mp.put(mapa_vertices, id, vertice)  # Se agrega el vertice al mapa de vertices
            
            gr.insertVertex(data_structs["distancias"], id) # Se agrega el vertice al grafo de distancias
            gr.insertVertex(data_structs["comparendos"], id) # Se agrega el vertice al grafo de comparendos
            
           
        case "estacionpolicia_bogota_vertices.csv":
            
            vertice_mas_cercano = data["VERTICES"]
            if mp.contains(mapa_vertices, vertice_mas_cercano):
                entrada_vertice =  mp.get(mapa_vertices, vertice_mas_cercano)
                vertice = me.getValue(entrada_vertice)
                lt.addLast(vertice["estaciones"], data)
                
                
            
        case 'comparendos_2019_bogota_vertices.csv':
            
        # ================================================ Carga Normal ================================================ #    
            
            id_vertice_mas_cercano = data["VERTICES"]
            if mp.contains(mapa_vertices, id_vertice_mas_cercano):
                entrada_vertice =  mp.get(mapa_vertices, id_vertice_mas_cercano)
                vertice = me.getValue(entrada_vertice)
                lt.addLast(vertice["comparendos"], data)
            
        # ================================================ Carga Mapa Localidades ================================================ #
            if mp.contains(mapa_localidades, data["LOCALIDAD"]): # Si el mapa de vehiculos contiene el vehiculo
                entrada_localidad = mp.get(mapa_localidades, data["LOCALIDAD"]) # Se obtiene la pareja {llave: vehiculo, valor: mapa_vertices_vehiculo}
                mapa_vertices_localidad = me.getValue(entrada_localidad) # Se obtiene el mapa de vertices del vehiculo
                
                if mp.contains(mapa_vertices_localidad, id_vertice_mas_cercano): # Si el mapa de vertices del vehiculo contiene el vertice más cercano
                    entrada_lista_comparendos = mp.get(mapa_vertices_localidad, id_vertice_mas_cercano) # Se obtiene la pareja {llave: id_vertice_mas_cercano, valor: lista_comparendos}
                    lista_comparendos = me.getValue(entrada_lista_comparendos) # Se obtiene la lista de comparendos del vertice más cercano
                    lt.addLast(lista_comparendos, data) # Se agrega el comparendo a la lista de comparendos del vertice más cercano
                
                else: # Si el mapa de vertices del vehiculo no contiene el vertice más cercano
                    lista_comparendos = lt.newList("ARRAY_LIST") # Se crea una lista de comparendos
                    lt.addLast(lista_comparendos, data) # Se agrega el comparendo a la lista de comparendos
                    mp.put(mapa_vertices_localidad, id_vertice_mas_cercano, lista_comparendos) # Se agrega la lista de comparendos al mapa de vertices del vehiculo
            
            else: # Si el mapa de vehiculos no contiene el vehiculo
                mapa_vertices_localidad = mp.newMap(numelements=54209, maptype="PROBING", loadfactor=0.5) # Se crea un mapa de vertices del vehiculo
                lista_comparendos = lt.newList("ARRAY_LIST") # Se crea una lista de comparendos
                lt.addLast(lista_comparendos, data) # Se agrega el comparendo a la lista de comparendos
                mp.put(mapa_vertices_localidad, id_vertice_mas_cercano, lista_comparendos) # Se agrega la lista de comparendos al mapa de vertices del vehiculo
                mp.put(mapa_localidades, data["LOCALIDAD"], mapa_vertices_localidad) # Se agrega el mapa de vertices del vehiculo al mapa de vehiculos
                
                

        # ============================================ Carga Mapa Vehiculos ============================================ #     
                
            if mp.contains(mapa_vehiculos, data["CLASE_VEHICULO"]): # Si el mapa de vehiculos contiene el vehiculo
                entrada_vehiculo = mp.get(mapa_vehiculos, data["CLASE_VEHICULO"]) # Se obtiene la pareja {llave: vehiculo, valor: mapa_vertices_vehiculo}
                mapa_vertices_vehiculo = me.getValue(entrada_vehiculo) # Se obtiene el mapa de vertices del vehiculo
                
                if mp.contains(mapa_vertices_vehiculo, id_vertice_mas_cercano): # Si el mapa de vertices del vehiculo contiene el vertice más cercano
                    entrada_lista_comparendos = mp.get(mapa_vertices_vehiculo, id_vertice_mas_cercano) # Se obtiene la pareja {llave: id_vertice_mas_cercano, valor: lista_comparendos}
                    lista_comparendos = me.getValue(entrada_lista_comparendos) # Se obtiene la lista de comparendos del vertice más cercano
                    lt.addLast(lista_comparendos, data) # Se agrega el comparendo a la lista de comparendos del vertice más cercano
                
                else: # Si el mapa de vertices del vehiculo no contiene el vertice más cercano
                    lista_comparendos = lt.newList("ARRAY_LIST") # Se crea una lista de comparendos
                    lt.addLast(lista_comparendos, data) # Se agrega el comparendo a la lista de comparendos
                    mp.put(mapa_vertices_vehiculo, id_vertice_mas_cercano, lista_comparendos) # Se agrega la lista de comparendos al mapa de vertices del vehiculo
            
            else: # Si el mapa de vehiculos no contiene el vehiculo
                mapa_vertices_vehiculo = mp.newMap(numelements=54209, maptype="PROBING", loadfactor=0.5) # Se crea un mapa de vertices del vehiculo
                lista_comparendos = lt.newList("ARRAY_LIST") # Se crea una lista de comparendos
                lt.addLast(lista_comparendos, data) # Se agrega el comparendo a la lista de comparendos
                mp.put(mapa_vertices_vehiculo, id_vertice_mas_cercano, lista_comparendos) # Se agrega la lista de comparendos al mapa de vertices del vehiculo
                mp.put(mapa_vehiculos, data["CLASE_VEHICULO"], mapa_vertices_vehiculo) # Se agrega el mapa de vertices del vehiculo al mapa de vehiculos
                
        # ============================================ Carga Mapa Gravedad ============================================ #
            servicio_infraccion = " ".join([data["TIPO_SERVICIO"], data["INFRACCION"]])
            if om.contains(mapa_gravedad_comparendos, servicio_infraccion): # Si el mapa de gravedad contiene la gravedad
                entrada_gravedad = om.get(mapa_gravedad_comparendos, servicio_infraccion)
                mapa_vertices_gravedad = me.getValue(entrada_gravedad)
                
                if mp.contains(mapa_vertices_gravedad, id_vertice_mas_cercano):
                    entrada_lista_comparendos = mp.get(mapa_vertices_gravedad, id_vertice_mas_cercano)
                    lista_comparendos = me.getValue(entrada_lista_comparendos)
                    lt.addLast(lista_comparendos, data)
                    
                else:
                    lista_comparendos = lt.newList("ARRAY_LIST")
                    lt.addLast(lista_comparendos, data)
                    mp.put(mapa_vertices_gravedad, id_vertice_mas_cercano, lista_comparendos)
                
            else: # Si el mapa de gravedad no contiene la gravedad
                mapa_vertices_gravedad = mp.newMap(numelements=54209, maptype="PROBING", loadfactor=0.5)
                lista_comparendos = lt.newList("ARRAY_LIST")
                lt.addLast(lista_comparendos, data)
                mp.put(mapa_vertices_gravedad, id_vertice_mas_cercano, lista_comparendos)
                om.put(mapa_gravedad_comparendos, servicio_infraccion, mapa_vertices_gravedad)
                
                
                        
        case "bogota_arcos.txt":
            data = data.split() # Se formatea la información de string "# # #" a lista ["#", "#", "#"]
            id_origen = data[0] # Se obtiene el id del vertice origen en la primera posición de la lista
            ids_destino = data[1:] # Se obtiene el id del vertice destino en la segunda posición de la lista
            
            entrada_vertice_origen = mp.get(mapa_vertices, id_origen)
            vertice_origen = me.getValue(entrada_vertice_origen)
            
            longitud_origen = vertice_origen["long"]
            latitud_origen = vertice_origen["lat"]
            estaciones_origen = vertice_origen["estaciones"]
            n_estaciones_origen = lt.size(estaciones_origen)
            
            
            for id_destino in ids_destino:
                
                
                entrada_vertice_destino = mp.get(mapa_vertices, id_destino)
                vertice_destino = me.getValue(entrada_vertice_destino)
                
                latitud_destino = vertice_destino["lat"]
                longitud_destino = vertice_destino["long"]
                comparendos_destino = vertice_destino["comparendos"]
                
                peso_distancia = haversine(latitud_origen, longitud_origen, latitud_destino, longitud_destino)
                n_comparendos_destino = lt.size(comparendos_destino)
                
                peso_comparendos = n_comparendos_destino + n_estaciones_origen
                
        
                gr.addEdge(data_structs["distancias"], id_origen, id_destino, peso_distancia) # Se agrega el arco al grafo de distancias
                
                
                gr.addEdge(data_structs["comparendos"], id_origen, id_destino, peso_comparendos) # Se agrega el arco al grafo de comparendos
            
    
    
def min_pq_localidades_comparendos(data_structs):
    mapa_localidades = data_structs["mapa_localidades"]
    mapa_localidades_max_pq = data_structs["mapa_localidades_maxpq_comparendos"]
    
    llaves_localidades = mp.keySet(mapa_localidades) # Se obtienen las llaves de mapa de vehiculos
    for llave_localidad in lt.iterator(llaves_localidades): # Para cada vehiculo en el mapa de vehiculos
        entrada_mapa_localidades = mp.get(mapa_localidades, llave_localidad) # Se obtiene la pareja {llave: vehiculo, valor: mapa de vertices del vehiculo}
        mapa_vertices_localidad = me.getValue(entrada_mapa_localidades) # Se obtiene el mapa de vertices del vehiculo

        llaves_vertices_localidad = mp.keySet(mapa_vertices_localidad) # Se obtienen las llaves del mapa de vertices del vehiculo
        for llave_vertice in lt.iterator(llaves_vertices_localidad): # Para cada vertice en el mapa de vertices del vehiculo
            entrada_mapa_vertices_localidad = mp.get(mapa_vertices_localidad, llave_vertice) # Se obtiene la pareja {llave: vertice, valor: lista_comparendos}
            lista_comparendos = me.getValue(entrada_mapa_vertices_localidad) # Se obtiene la lista de comparendos del vertice
            num_comparendos = lt.size(lista_comparendos) # Se obtiene el número de comparendos del vertice
        
            if mp.contains(mapa_localidades_max_pq, llave_localidad): # Si el mapa de vehiculos con max_pq de comparendos contiene el vehiculo  
                entrada_mapa_localidades_maxpq_comparendos = mp.get(mapa_localidades_max_pq, llave_localidad) # Se obtiene la pareja {llave: vehiculo, valor: max_pq_comparendos}
                max_pq_comparendos = me.getValue(entrada_mapa_localidades_maxpq_comparendos) # Se obtiene la max_pq de comparendos del vehiculo
                
                impq.insert(max_pq_comparendos, llave_vertice, -num_comparendos) # Se agrega el vertice a la max_pq de comparendos del vehiculo
            
            else: # Si el mapa de vehiculos con max_pq de comparendos no contiene el vehiculo
                max_pq_comparendos = impq.newIndexMinPQ(cmpfunction=compare_num_comparendos) # Se crea una max_pq de comparendos
                impq.insert(max_pq_comparendos, llave_vertice, -num_comparendos) # Se agrega el vertice a la max_pq de comparendos del vehiculo
                mp.put(mapa_localidades_max_pq, llave_localidad, max_pq_comparendos) # Se agrega el max_pq de comparendos al mapa de vehiculos con max_pq de comparendos      

def min_pq_vehiculo_comparendos(data_structs):
    mapa_vehiculos = data_structs["mapa_vehiculos"]
    mapa_vehiculos_maxpq_comparendos = data_structs["mapa_vehiculos_maxpq_comparendos"]
    
    llaves_vehiculos = mp.keySet(mapa_vehiculos) # Se obtienen las llaves de mapa de vehiculos
    for llave_vehiculo in lt.iterator(llaves_vehiculos): # Para cada vehiculo en el mapa de vehiculos
        entrada_mapa_vehiculos = mp.get(mapa_vehiculos, llave_vehiculo) # Se obtiene la pareja {llave: vehiculo, valor: mapa de vertices del vehiculo}
        mapa_vertices_vehiculo = me.getValue(entrada_mapa_vehiculos) # Se obtiene el mapa de vertices del vehiculo

        llaves_vertices_vehiculo = mp.keySet(mapa_vertices_vehiculo) # Se obtienen las llaves del mapa de vertices del vehiculo
        for llave_vertice in lt.iterator(llaves_vertices_vehiculo): # Para cada vertice en el mapa de vertices del vehiculo
            entrada_mapa_vertices_vehiculo = mp.get(mapa_vertices_vehiculo, llave_vertice) # Se obtiene la pareja {llave: vertice, valor: lista_comparendos}
            lista_comparendos = me.getValue(entrada_mapa_vertices_vehiculo) # Se obtiene la lista de comparendos del vertice
            num_comparendos = lt.size(lista_comparendos) # Se obtiene el número de comparendos del vertice
        
            if mp.contains(mapa_vehiculos_maxpq_comparendos, llave_vehiculo): # Si el mapa de vehiculos con max_pq de comparendos contiene el vehiculo  
                entrada_mapa_vehiculos_maxpq_comparendos = mp.get(mapa_vehiculos_maxpq_comparendos, llave_vehiculo) # Se obtiene la pareja {llave: vehiculo, valor: max_pq_comparendos}
                max_pq_comparendos = me.getValue(entrada_mapa_vehiculos_maxpq_comparendos) # Se obtiene la max_pq de comparendos del vehiculo
                
                impq.insert(max_pq_comparendos, llave_vertice, -num_comparendos) # Se agrega el vertice a la max_pq de comparendos del vehiculo
            
            else: # Si el mapa de vehiculos con max_pq de comparendos no contiene el vehiculo
                max_pq_comparendos = impq.newIndexMinPQ(cmpfunction=compare_num_comparendos) # Se crea una max_pq de comparendos
                impq.insert(max_pq_comparendos, llave_vertice, -num_comparendos) # Se agrega el vertice a la max_pq de comparendos del vehiculo
                mp.put(mapa_vehiculos_maxpq_comparendos, llave_vehiculo, max_pq_comparendos) # Se agrega el max_pq de comparendos al mapa de vehiculos con max_pq de comparendos

          
def min_pq_gravedad_comparendos(data_structs):
    mapa_gravedad_comparendos = data_structs["mapa_gravedad_comparendos"] 
    mapa_gravedad_maxpq_comparendos = data_structs["mapa_gravedad_maxpq_comparendos"]
    
    llaves_gravedad = om.keySet(mapa_gravedad_comparendos) # Se obtienen las llaves del mapa de gravedad
    for llave_gravedad in lt.iterator(llaves_gravedad): # Para cada gravedad en el mapa de gravedad
        entrada_mapa_gravedad = om.get(mapa_gravedad_comparendos, llave_gravedad) # Se obtiene la pareja {llave: gravedad, valor: mapa de vertices de la gravedad}
        mapa_vertices_gravedad = me.getValue(entrada_mapa_gravedad) # Se obtiene el mapa de vertices de la gravedad
        
        llaves_vertices_gravedad = mp.keySet(mapa_vertices_gravedad) # Se obtienen las llaves del mapa de vertices de la gravedad
        for llave_vertice in lt.iterator(llaves_vertices_gravedad): # Para cada vertice en el mapa de vertices de la gravedad
            entrada_mapa_vertices_gravedad = mp.get(mapa_vertices_gravedad, llave_vertice) # Se obtiene la pareja {llave: vertice, valor: lista_comparendos}
            lista_comparendos = me.getValue(entrada_mapa_vertices_gravedad) # Se obtiene la lista de comparendos del vertice
            
            for comparendo in lt.iterator(lista_comparendos): # Para cada comparendo en la lista de comparendos del vertice
                gravedad = " ".join([comparendo["TIPO_SERVICIO"], comparendo["INFRACCION"]]) # Se obtiene la gravedad del comparendo
                orden_gravedad = get_orden_gravedad(gravedad) # Se obtiene el orden de la gravedad
                
                if mp.contains(mapa_gravedad_maxpq_comparendos, gravedad): # Si el mapa de gravedad con max_pq de comparendos contiene la gravedad  
                    entrada_mapa_gravedad_maxpq_comparendos = mp.get(mapa_gravedad_maxpq_comparendos, gravedad) # Se obtiene la pareja {llave: gravedad, valor: max_pq_comparendos}
                    max_pq_comparendos = me.getValue(entrada_mapa_gravedad_maxpq_comparendos) # Se obtiene la max_pq de comparendos de la gravedad
                    
                    impq.insert(max_pq_comparendos, llave_vertice, orden_gravedad) # Se agrega el vertice a la max_pq de comparendos de la gravedad
                    
                else: # Si el mapa de gravedad con max_pq de comparendos no contiene la gravedad
                    max_pq_comparendos = impq.newIndexMinPQ(cmpfunction=compare_gravedad_pq)
                    impq.insert(max_pq_comparendos, llave_vertice, orden_gravedad) # Se agrega el vertice a la max_pq de comparendos de la gravedad
                    mp.put(mapa_gravedad_maxpq_comparendos, gravedad, max_pq_comparendos) # Se agrega el max_pq de comparendos al mapa de gravedad con max_pq de comparendos
                
        

                    
def new_data_req5(vertice):
    """
    Crea un nuevo dato
    """
    
    dato = {"id": vertice["id"],
            "long": vertice["long"],
            "lat": vertice["lat"],
            "num_comparendos": 1,
            }
    
    return dato
            
    
def new_reduced_data(vertice):
    
    dato = {"id": vertice["id"],
            "long": vertice["long"],
            "lat": vertice["lat"],}
    
    return dato
            
        
    


# Funciones para creacion de datos



def get_orden_gravedad(codigo_gravedad):
    """
    Retorna un dato a partir de su ID
    """
    
    orden_gravedad = []
    
    codigo_gravedad = codigo_gravedad.split(" ")
    if codigo_gravedad[0] == "Particular":
        valor_1 = -1
    elif codigo_gravedad[0] == "Oficial":
        valor_1 = -2
    elif codigo_gravedad[0] == "Público":    
        valor_1 = -3
    else:
        valor_1 = 0
    orden_gravedad.append(valor_1)
    
    
    if codigo_gravedad[1] == "F":
        codigo_gravedad[1] = "F00"
        
    for caracter in codigo_gravedad[1]:
        valor_2 = []
        valor_2.append(-ord(caracter))
        
    orden_gravedad.append(valor_2)
    
    return orden_gravedad
        


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs, latitud_vertice_origen, longitud_vertice_origen, latitud_vertice_destino, longitud_vertice_destino):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1

    mapa_vertices = data_structs["mapa_vertices"]
    distancias = data_structs["distancias"]
    

    
    llaves_mapa_vertices = mp.keySet(mapa_vertices)
    vertice_mas_cercano_origen = None
    vertice_mas_cercano_destino = None
    distancia_minima_origen = float("inf")
    distancia_minima_destino = float("inf")
    
    for vertice_id in lt.iterator(llaves_mapa_vertices):
        entrada_vertice = mp.get(mapa_vertices, vertice_id)
        vertice = me.getValue(entrada_vertice)
        
        latitud_vertice = vertice["lat"]
        longitud_vertice = vertice["long"]
        
        distancia_origen = haversine(latitud_vertice_origen, longitud_vertice_origen, latitud_vertice, longitud_vertice)
        distancia_destino = haversine(latitud_vertice_destino, longitud_vertice_destino, latitud_vertice, longitud_vertice)
        
        if distancia_origen < distancia_minima_origen:
            distancia_minima_origen = distancia_origen
            vertice_mas_cercano_origen = vertice_id
            
        if distancia_destino < distancia_minima_destino:
            distancia_minima_destino = distancia_destino
            vertice_mas_cercano_destino = vertice_id

    search = bfs.BreadhtFisrtSearch(distancias, vertice_mas_cercano_origen)
    pathTo = bfs.pathTo(search, vertice_mas_cercano_destino)
    

    total_vertices = pathTo["size"]
    
    total_distancia = 0
    for i in range(total_vertices-1):
        vertice_id = lt.getElement(pathTo, i)
        vertice = me.getValue(mp.get(mapa_vertices, vertice_id))
        vertice_id_siguiente = lt.getElement(pathTo, i+1)
        vertice_siguiente = me.getValue(mp.get(mapa_vertices, vertice_id_siguiente))
        
        distancia = haversine(vertice["lat"], vertice["long"], vertice_siguiente["lat"], vertice_siguiente["long"])
        total_distancia += distancia
        
    return total_vertices, total_distancia, pathTo
def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs, n_camaras, localidad):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    
    mapa_localidades_maxpq_comparendos = data_structs["mapa_localidades_maxpq_comparendos"]
    mapa_vertices = data_structs["mapa_vertices"]
    
    entrada_mapa_localidad = mp.get(mapa_localidades_maxpq_comparendos, localidad)
    max_pq_comparendos = me.getValue(entrada_mapa_localidad)
    
    sub_grafo = gr.newGraph(datastructure="ADJ_LIST", directed=False)
    sub_mapa = mp.newMap(numelements=120000, maptype="PROBING", loadfactor=0.5)
    
    for i in range(n_camaras): # Para cada camara solicitada
        id_vertice = impq.min(max_pq_comparendos) # Se obtiene el id del vertice con mayor número de comparendos
        impq.delMin(max_pq_comparendos) # Se elimina el vertice con mayor número de comparendos de la max_pq de comparendos
        entrada_mapa_vertices = mp.get(mapa_vertices, id_vertice) # Se obtiene la pareja {llave: id_vertice, valor: vertice}
        vertice = me.getValue(entrada_mapa_vertices) # Se obtiene el vertice
        
        vertice_grafo = new_reduced_data(vertice) # Se crea un vertice con la información del vertice pertinente
        mp.put(sub_mapa, id_vertice, vertice_grafo) # Se agrega el vertice al mapa de vertices del subgrafo
        gr.insertVertex(sub_grafo, vertice_grafo["id"]) # Se agrega el vertice al subgrafo
    i = 0    
    vertices_llaves = mp.keySet(sub_mapa) # Se obtienen las llaves del mapa de vertices del subgrafo
    for llave_vertice in lt.iterator(vertices_llaves): # Para cada vertice en el mapa de vertices del subgrafo
        entrada_mapa_vertices = mp.get(sub_mapa, llave_vertice) # Se obtiene la pareja {llave: id_vertice, valor: vertice}
        vertice = me.getValue(entrada_mapa_vertices) # Se obtiene el vertice
        size = lt.size(vertices_llaves) # Se obtiene el tamaño de la lista de vertices del subgrafo
        
        posicion_vertice = lt.isPresent(vertices_llaves, llave_vertice) # Se obtiene la posición del vertice en la lista de vertices del subgrafo
        if posicion_vertice != 0: # Si el vertice está en la lista de vertices del subgrafo
            demas_vertices = lt.subList(vertices_llaves, posicion_vertice, size+i) # Se obtienen los vertices restantes en la lista de vertices del subgrafo
            
        for llave_demas_vertice in lt.iterator(demas_vertices):
            entrada_llave_demas_vertice = mp.get(sub_mapa, llave_demas_vertice) # Se obtiene la pareja {llave: id_vertice, valor: vertice}
            llave_demas_vertice = me.getValue(entrada_llave_demas_vertice) # Se obtiene el vertice
            distancia = haversine(vertice["lat"], vertice["long"], llave_demas_vertice["lat"], llave_demas_vertice["long"]) # Se calcula la distancia entre el vertice y los demás vertices del subgrafo
            gr.addEdge(sub_grafo, vertice["id"], llave_demas_vertice["id"], distancia) # Se agregan los arcos entre el vertice y los demás vertices del subgrafo
        i -= 1 
           
    origen = lt.firstElement(vertices_llaves) # Se obtiene el primer vertice de la lista de vertices del subgrafo    
    mst = prim.PrimMST(sub_grafo, origin=origen) # Se obtiene el MST del subgrafo
    mst_grafo = prim.prim(sub_grafo, mst, origen) # Se obtiene el grafo con los arcos del recorrdio del MST
    total_camaras = lt.size(vertices_llaves) 
    id_vertices = vertices_llaves 
    arcos = prim.edgesMST(sub_grafo, mst) # Se obtienen los arcos del MST
    extension =  prim.weightMST(sub_grafo, mst) # Se obtienen los arcos del MST
    
    costo = extension * 1000000
    
    return total_camaras, id_vertices, arcos, extension, costo



def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs, n_camaras, clase_vehiculo):
    """
    Función que soluciona el requerimiento 5
    """
    # try:
    mapa_vehiculos_maxpq_comparendos = data_structs["mapa_vehiculos_maxpq_comparendos"]
    mapa_vertices = data_structs["mapa_vertices"]
    
    entrada_mapa_vehiculo = mp.get(mapa_vehiculos_maxpq_comparendos, clase_vehiculo)
    max_pq_comparendos = me.getValue(entrada_mapa_vehiculo)
    
    sub_grafo = gr.newGraph(datastructure="ADJ_LIST", directed=False)
    sub_mapa = mp.newMap(numelements=120000, maptype="PROBING", loadfactor=0.5)
    
    for i in range(n_camaras): # Para cada camara solicitada
        id_vertice = impq.min(max_pq_comparendos) # Se obtiene el id del vertice con mayor número de comparendos
        impq.delMin(max_pq_comparendos) # Se elimina el vertice con mayor número de comparendos de la max_pq de comparendos
        entrada_mapa_vertices = mp.get(mapa_vertices, id_vertice) # Se obtiene la pareja {llave: id_vertice, valor: vertice}
        vertice = me.getValue(entrada_mapa_vertices) # Se obtiene el vertice
        
        vertice_grafo = new_reduced_data(vertice) # Se crea un vertice con la información del vertice pertinente
        mp.put(sub_mapa, id_vertice, vertice_grafo) # Se agrega el vertice al mapa de vertices del subgrafo
        gr.insertVertex(sub_grafo, vertice_grafo["id"]) # Se agrega el vertice al subgrafo
    i = 0    
    vertices_llaves = mp.keySet(sub_mapa) # Se obtienen las llaves del mapa de vertices del subgrafo
    for llave_vertice in lt.iterator(vertices_llaves): # Para cada vertice en el mapa de vertices del subgrafo
        entrada_mapa_vertices = mp.get(sub_mapa, llave_vertice) # Se obtiene la pareja {llave: id_vertice, valor: vertice}
        vertice = me.getValue(entrada_mapa_vertices) # Se obtiene el vertice
        size = lt.size(vertices_llaves) # Se obtiene el tamaño de la lista de vertices del subgrafo
        
        posicion_vertice = lt.isPresent(vertices_llaves, llave_vertice) # Se obtiene la posición del vertice en la lista de vertices del subgrafo
        if posicion_vertice != 0: # Si el vertice está en la lista de vertices del subgrafo
            demas_vertices = lt.subList(vertices_llaves, posicion_vertice, size+i) # Se obtienen los vertices restantes en la lista de vertices del subgrafo
            
        for llave_demas_vertice in lt.iterator(demas_vertices):
            entrada_llave_demas_vertice = mp.get(sub_mapa, llave_demas_vertice) # Se obtiene la pareja {llave: id_vertice, valor: vertice}
            llave_demas_vertice = me.getValue(entrada_llave_demas_vertice) # Se obtiene el vertice
            distancia = haversine(vertice["lat"], vertice["long"], llave_demas_vertice["lat"], llave_demas_vertice["long"]) # Se calcula la distancia entre el vertice y los demás vertices del subgrafo
            gr.addEdge(sub_grafo, vertice["id"], llave_demas_vertice["id"], distancia) # Se agregan los arcos entre el vertice y los demás vertices del subgrafo
        i -= 1 
           
    origen = lt.firstElement(vertices_llaves) # Se obtiene el primer vertice de la lista de vertices del subgrafo    
    mst = prim.PrimMST(sub_grafo, origin=origen) # Se obtiene el MST del subgrafo
    mst_grafo = prim.prim(sub_grafo, mst, origen) # Se obtiene el grafo con los arcos del recorrdio del MST
    total_camaras = lt.size(vertices_llaves) 
    id_vertices = vertices_llaves 
    arcos = prim.edgesMST(sub_grafo, mst) # Se obtienen los arcos del MST
    extension =  prim.weightMST(sub_grafo, mst) # Se obtienen los arcos del MST
    
    costo = extension * 1000000
    
    return total_camaras, id_vertices, arcos, extension, costo
    
    # except Exception as exp:
    #     print("Error: {}".format(exp))
    #     return None, None, None, None, None
    
        
    
        
        

        
        
        
        
    


def req_6(data_structs, num_comparendos_graves):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    mapa_gravedad_comparendos = data_structs["mapa_gravedad_comparendos"]
    mapa_vertices = data_structs["mapa_vertices"]
    
    llaves_mapa_gravedad = om.keySet(mapa_gravedad_comparendos) # Se obtienen las llaves del mapa de gravedad
    mapa_vertice_cercano_comparendo_grave = mp.newMap(numelements=100000, maptype="PROBING", loadfactor=0.5) # Mapa: {llave: id_vertice, valor: vertice}
    valores_mapa_gravedad = 0
    
    i = 1
    while i < num_comparendos_graves:
        for gravedad in lt.iterator(llaves_mapa_gravedad): # Para cada gravedad en el mapa de gravedad
            entrada_gravedad_comparendos = mp.get(mapa_gravedad_comparendos, gravedad) # Se obtiene la pareja {llave: gravedad, valor: lista_comparendos}
            lista_comparendos = me.getValue(entrada_gravedad_comparendos) # Se obtiene la lista de comparendos de la gravedad
            
            if lt.size(lista_comparendos) >= i: # Si la lista de comparendos de la gravedad tiene más de i comparendos
                comparendo = lt.getElement(lista_comparendos, i) # Se obtiene el comparendo en la posición i de la lista de comparendos de la gravedad
                vertice_mas_cercano = comparendo["VERTICES"] # Se obtiene el id del vertice más cercano al comparendo
                    
                    
                
                
        
    
    
  
        


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare_num_comparendos(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    data_1 = int(data_1)
    data_2 =  int(data_2['key'])
    
    if data_1 > data_2:
        return 1
    elif data_1 < data_2:
        return -1
    else:
        return 0
 
def compare_gravedad(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    data_1 = get_orden_gravedad(data_1)
    data_2 =  get_orden_gravedad(data_2)
    
    if data_1 > data_2:
        return 1
    elif data_1 < data_2:
        return -1
    else:
        return 0
    
   
def compare_gravedad_pq(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    data_1 = (data_1)
    data_2 = (data_2['key'])

    if data_1 > data_2:
        return 1
    elif data_1 < data_2:
        return -1
    else:
        return 0

# Funciones de ordenamiento


    
    


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass


def haversine(lat1, lon1, lat2, lon2):
    """
    Función que calcula la distancia entre dos puntos en la tierra
    """
    radio_tierra = 6371
    lat1 = mt.radians(lat1)
    lon1 = mt.radians(lon1)
    lat2 = mt.radians(lat2)
    lon2 = mt.radians(lon2)
    
    distancia = 2 * radio_tierra * mt.asin(mt.sqrt(mt.sin((lat2-lat1)/2)**2 + mt.cos(lat1) * mt.cos(lat2) * mt.sin((lon2-lon1)/2)**2))
    
    return distancia


