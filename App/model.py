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
                    "mapa_vertices": None, # Mapa: {id: vertice}
                    "mapa_vehiculos_maxpq_comparendos": None, # Mapa: {llave: vehiculo, valor: max_pq_comparendos}
                   
                    
        
                    }
    
    
    data_structs["comparendos"] = gr.newGraph(datastructure="ADJ_LIST", directed=False)
    
    data_structs["distancias"] = gr.newGraph(datastructure="ADJ_LIST", directed=False)
    
    data_structs["mapa_vertices"] = mp.newMap(numelements=228045, maptype="PROBING", loadfactor=0.5)
    
    data_structs["mapa_vehiculos_maxpq_comparendos"] = mp.newMap(numelements=35, maptype="PROBING", loadfactor=0.5)
    
    data_structs["mapa_vehiculos"] = mp.newMap(numelements=35, maptype="PROBING", loadfactor=0.5)
    
    
    
    return data_structs
    


# Funciones para agregar informacion al modelo

def add_data(data_structs, archivo, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    mapa_vertices = data_structs["mapa_vertices"] # Mapa: {id: vertice}
    mapa_vehiculos = data_structs["mapa_vehiculos"] # Mapa: {llave: vehiculo, valor: }
    
    
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
                      
            id_vertice_mas_cercano = data["VERTICES"]
            if mp.contains(mapa_vertices, id_vertice_mas_cercano):
                entrada_vertice =  mp.get(mapa_vertices, id_vertice_mas_cercano)
                vertice = me.getValue(entrada_vertice)
                lt.addLast(vertice["comparendos"], data)
            
                
            if mp.contains(mapa_vehiculos, data["CLASE_VEHICULO"]):
                entrada_vehiculo = mp.get(mapa_vehiculos, data["CLASE_VEHICULO"])
                mapa_vertices_vehiculo = me.getValue(entrada_vehiculo)
                
                if mp.contains(mapa_vertices_vehiculo, id_vertice_mas_cercano):
                    entrada_lista_comparendos = mp.get(mapa_vertices_vehiculo, id_vertice_mas_cercano)
                    lista_comparendos = me.getValue(entrada_lista_comparendos)
                    lt.addLast(lista_comparendos, data)
                else:
                    lista_comparendos = lt.newList("ARRAY_LIST")
                    lt.addLast(lista_comparendos, data)
                    mp.put(mapa_vertices_vehiculo, id_vertice_mas_cercano, lista_comparendos)
            
            else:
                mapa_vertices_vehiculo = mp.newMap(numelements=100000, maptype="PROBING", loadfactor=0.5)
                lista_comparendos = lt.newList("ARRAY_LIST")
                lt.addLast(lista_comparendos, data)
                mp.put(mapa_vertices_vehiculo, id_vertice_mas_cercano, lista_comparendos)    
                mp.put(mapa_vehiculos, data["CLASE_VEHICULO"], mapa_vertices_vehiculo)

                
                        
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



def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


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
    mst_grafo = prim.prim(sub_grafo, mst, origen) # Se obtiene el MST del subgrafo
    total_camaras = lt.size(vertices_llaves) 
    id_vertices = vertices_llaves 
    arcos =  gr.edges(mst_grafo) # Se obtienen los arcos del MST
    
    extension = 0
    for arco in lt.iterator(arcos):
        extension += arco
    
    costo = extension * 1000000
    
    return total_camaras, id_vertices, arcos, extension, costo
    
    # except Exception as exp:
    #     print("Error: {}".format(exp))
    #     return None, None, None, None, None
    
        
    
        
        

        
        
        
        
    


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


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


