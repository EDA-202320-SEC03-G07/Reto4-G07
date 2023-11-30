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
                    "mapa_areas": None, # Mapa: {area: lista de vertices}
                    
                    "lat_max": float("-inf"), # Latitud máxima	
                    "lat_min": float("inf"), # Latitud mínima
                    "long_max": float("-inf"), # Longitud máxima
                    "long_min": float("inf"), # Longitud mínima
                    
                    "long_mid": 0, # Punto medio de la longitud
                    "lat_mid": 0, # Punto medio de la latitud
                    
        
                    }
    
    
    data_structs["comparendos"] = gr.newGraph(datastructure="ADJ_LIST", directed=False)
    
    data_structs["distancias"] = gr.newGraph(datastructure="ADJ_LIST", directed=False)
    
    data_structs["mapa_vertices"] = mp.newMap(numelements=228045, maptype="PROBING", loadfactor=0.5)
    
    data_structs["mapa_areas"] = mp.newMap(numelements=4, maptype="PROBING", loadfactor=0.5)
    
    
    
    


# Funciones para agregar informacion al modelo

def add_data(data_structs, archivo, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    mapa_vertices = data_structs["mapa_vertices"] # Mapa: {id: vertice}
    
    long_max = data_structs["long_max"] 
    long_min = data_structs["long_min"]
    
    lat_max = data_structs["lat_max"]
    lat_min = data_structs["lat_min"]
    
    long_mid = data_structs["long_mid"]
    lat_mid = data_structs["lat_mid"]
    
    
    match archivo:
        case "bogota_vertices.txt": # Se agrega un vertice al mapa de vertices
            data = data.split(" ") # Se formatea la información de string "# # #" a lista ["#", "#", "#"]
            id = data[0] # Se obtiene el id del vertice en la primera posición de la lista
            longitud = data[1] # Se obtiene la longitud del vertice en la segunda posición de la lista
            latitud = data[2] # Se obtiene la latitud del vertice en la tercera posición de la lista
            
            
            # Se crea un vertice con la información obtenida en formato dict
            vertice = {"long": longitud, 
                       "lat": latitud,
                       "estaciones": lt.newList("ARRAY_LIST"), # Lista de estaciones de policia más cercanas al vertice. Una si es única, varias si hay empate
                       "comparendos": lt.newList("ARRAY_LIST"), # Lista de comparendos en el vertice
                       }
            
            
            mp.put(mapa_vertices, id, vertice)  # Se agrega el vertice al mapa de vertices
            
            gr.insertVertex(data_structs["distancias"], id) # Se agrega el vertice al grafo de distancias
            gr.insertVertex(data_structs["comparendos"], id) # Se agrega el vertice al grafo de comparendos
            
           
           # Acttualización de los valores máximos y mínimos de latitud y longitud
            if longitud > long_max:
                long_max = longitud
                
            if longitud < long_min:
                long_min = longitud 
                
            if latitud > lat_max:
                lat_max = latitud
                
            if latitud < lat_min:
                lat_min = latitud
             
            # Actualización de los puntos medios de latitud y longitud 
            long_mid = (long_max - long_min) / 2
            lat_mid = (lat_max - lat_min) / 2
            
            
                 
        case "estacionpolicia.json":
            
            area_seleccionada = None 
            
            entrada_lista_a1 = mp.get(data_structs["mapa_areas"], "a1")
            lista_a1 = me.getValue(entrada_lista_a1)
            
            entrada_lista_a2 = mp.get(data_structs["mapa_areas"], "a2")
            lista_a2 = me.getValue(entrada_lista_a2)
            
            entrada_lista_a3 = mp.get(data_structs["mapa_areas"], "a3")
            lista_a3 = me.getValue(entrada_lista_a3)
            
            entrada_lista_a4 = mp.get(data_structs["mapa_areas"], "a4")
            lista_a4 = me.getValue(entrada_lista_a4)
            
            posicion = data["EPOLONGITU"] > long_mid, data["EPOLATITUD"] > lat_mid
            
            
            match posicion:
                
                case True, True: # Cuadrante 1

                    area_seleccionada = lista_a1
                    
                case False, True: # Cuadrante 2
                    
                    area_seleccionada = lista_a2
                    
                case False, False: # Cuadrante 3
                    
                    area_seleccionada = lista_a3
                    
                case True, False: # Cuadrante 4
                    
                    area_seleccionada = lista_a4
            
            
            
            id_mas_cercano = None # id del vertice más cercano a la estación de policia inicializado en ninguno
            distancia_mas_cercano = float("inf") # Distancia más cercana inicializada en infinito
            for vertice_id in lt.iterator(area_seleccionada): # Para cada vertice en el cuadrante seleccionado
                entrada = mp.get(mapa_vertices, vertice_id) # Se obtiene la pareja {llave: id, valor: vertice}
                vertice = me.getValue(entrada) # Se obtiene el vertice de la pareja
                distancia = haversine(data["EPOLATITUD"], data["EPOLONGITU"], vertice["lat"], vertice["long"]) # Se calcula la distancia entre la estación de policia y el vertice
                
                if distancia < distancia_mas_cercano: # Si la distancia es menor a la distancia más cercana
                    distancia_mas_cercano = distancia # Se actualiza la distancia más cercana
                    id_mas_cercano = vertice_id # Se actualiza el id del vertice más cercano
            
            entrada = mp.get(mapa_vertices, id_mas_cercano) # Se obtiene la pareja {llave: id, valor: vertice}
            vertice = me.getValue(entrada) # Se obtiene el vertice de la pareja
            
        
            lt.addLast(vertice["estaciones"], data) # Se agrega la estación de policia a la lista de estaciones del vertice

                    
        
        case 'Comparendos_2019_Bogota_D_C.geojson':
            
            area_seleccionada = None
            
            entrada_lista_a1 = mp.get(data_structs["mapa_areas"], "a1")
            lista_a1 = me.getValue(entrada_lista_a1)
            
            entrada_lista_a2 = mp.get(data_structs["mapa_areas"], "a2")
            lista_a2 = me.getValue(entrada_lista_a2)
            
            entrada_lista_a3 = mp.get(data_structs["mapa_areas"], "a3")
            lista_a3 = me.getValue(entrada_lista_a3)
            
            entrada_lista_a4 = mp.get(data_structs["mapa_areas"], "a4")
            lista_a4 = me.getValue(entrada_lista_a4)
             
            posicion = data["LONGITUD"] > long_mid, data["LATITUD"] > lat_mid
            
            match posicion:
                
                case True, True: # Cuadrante 1

                    area_seleccionada = lista_a1
                    
                case False, True: # Cuadrante 2
                    
                    area_seleccionada = lista_a2
                    
                case False, False: # Cuadrante 3
                    
                    area_seleccionada = lista_a3
                    
                case True, False: # Cuadrante 4
                    
                    area_seleccionada = lista_a4
            
        
            id_mas_cercano = None # id del vertice más cercano al comparendo
            distancia_mas_cercano = float("inf") # Distancia más cercana inicializada en infinito
            for vertice_id in lt.iterator(area_seleccionada):
                entrada = mp.get(mapa_vertices, vertice_id)
                vertice = me.getValue(entrada)
                distancia = haversine(data["LATITUD"], data["LONGITUD"], vertice["lat"], vertice["long"])
                if distancia < distancia_mas_cercano:
                    distancia_mas_cercano = distancia
                    id_mas_cercano = vertice_id
            
            entrada = mp.get(mapa_vertices, id_mas_cercano)
            vertice = me.getValue(entrada)
            
            
            
            lt.addLast(vertice["comparendos"], data)
            
            
        case "bogota_arcos.txt":
            data = data.split(" ")
            id_origen = data[0]
            ids_adj = data[1:]
            
            for id_adj in ids_adj:
                
                entrada_vertice_origen = mp.get(mapa_vertices, id_origen)
                vertice_origen = me.getValue(entrada_vertice_origen)
                
                entrada_vertice_adj = mp.get(mapa_vertices, id_adj)
                vertice_adj = me.getValue(entrada_vertice_adj)
                
                
                peso_distancia = haversine(vertice_origen["lat"], vertice_origen["long"], vertice_adj["lat"], vertice_adj["long"])
                peso_comparendos = lt.size(vertice_origen["comparendo"]) + lt.size(vertice_adj["comparendo"])
                
                
                
                gr.addEdge(data_structs["distancias"], vertice_origen, vertice_adj, peso_distancia)
                gr.addEdge(data_structs["comparendos"], vertice_origen, vertice_adj, peso_comparendos)
                
            
            
        
            
        
def insert_aprox(data_structs):
    
    vertices = data_structs["mapa_vertices"] # Mapa: {llave:id, valor: vertice}
    
    mapa_areas = data_structs["mapa_areas"] # Mapa: {llave: area, valor: lista de vertices}
    
    vertices_ids = mp.keySet(vertices) # Lista de ids de los vertices
    
    long_mid = data_structs["long_mid"] # Punto medio de la longitud
    lat_mid = data_structs["lat_mid"] # Punto medio de la latitud
    
    
    for id in lt.iterator(vertices_ids): # Para cada id en el arreglo tipo lista de ids de los vertices
        entrada = mp.get(vertices, id) # Se obtiene pareja {llave: id, valor: vertice}
        vertice = me.getValue(entrada) # Se obtiene el vertice de la pareja
        vertice_long = vertice["long"] # Se obtiene la longitud del vertice
        vertice_lat = vertice["lat"] # Se obtiene la latitud del vertice
        

        posicion = vertice_long >= long_mid, vertice_lat >= lat_mid # Se determina la posición del vertice en el mapa de areas
        
        match posicion:
            
            case True, True: # Cuadrante 1
       
                if mp.contains(mapa_areas, "a1"): # Si el mapa de areas contiene el cuadrante 1
                    elemento = mp.get(mapa_areas, "a1") # Se obtiene la pareja {llave: "a1", valor: lista de vertices}
                    lista_area = me.getValue(elemento) # Se obtiene la lista de vertices de la pareja
                    lt.addLast(lista_area, id) # Se agrega el id del vertice a la lista de vertices del cuadrante 1
                        
                else: # Si el mapa de areas no contiene el cuadrante 1
                    info = lt.newList('ARRAY_LIST') # Se crea una lista vacía para los vertices del cuadrante 1
                    lt.addLast(info, id) # Se agrega el id del vertice a la lista vacía
                    mp.put(mapa_areas, "a1", id) # Se agrega la pareja {llave: "a1", valor: lista de vertices} al mapa de areas
            
            case False, True: # Cuadrante 2
                
                if mp.contains(mapa_areas, "a2"): # Si el mapa de areas contiene el cuadrante 2
                    elemento = mp.get(mapa_areas, "a2") # Se obtiene la pareja {llave: "a2", valor: lista de vertices}
                    lista_area = me.getValue(elemento) # Se obtiene la lista de vertices de la pareja
                    lt.addLast(lista_area, id) # Se agrega el id del vertice a la lista de vertices del cuadrante 2
                      
                else: # Si el mapa de areas no contiene el cuadrante 2
                    info = lt.newList('ARRAY_LIST') # Se crea una lista vacía para los vertices del cuadrante 2
                    lt.addLast(info, id) # Se agrega el id del vertice a la lista vacía
                    mp.put(data_structs["mapa_areas"], "a2", id) # Se agrega la pareja {llave: "a2", valor: lista de vertices} al mapa de areas
                    
            case False, False: # Cuadrante 3
                
                if mp.contains(mapa_areas, "a3"): # Si el mapa de areas contiene el cuadrante 3
                    elemento = mp.get(mapa_areas, "a3") # Se obtiene la pareja {llave: "a3", valor: lista de vertices}
                    lista_area = me.getValue(elemento) # Se obtiene la lista de vertices de la pareja
                    lt.addLast(lista_area, id) # Se agrega el id del vertice a la lista de vertices del cuadrante 3
                    
                else: # Si el mapa de areas no contiene el cuadrante 3
                    info = lt.newList('ARRAY_LIST') # Se crea una lista vacía para los vertices del cuadrante 3
                    lt.addLast(info, id) # Se agrega el id del vertice a la lista vacía
                    mp.put(data_structs["mapa_areas"], "a3", id) # Se agrega la pareja {llave: "a3", valor: lista de vertices} al mapa de areas
                    
            case True, False: # Cuadrante 4
                
                if mp.contains(mapa_areas, "a4"): # Si el mapa de areas contiene el cuadrante 4
                    elemento = mp.get(mapa_areas, "a4") # Se obtiene la pareja {llave: "a4", valor: lista de vertices}
                    lista_area = me.getValue(elemento) # Se obtiene la lista de vertices de la pareja
                    lt.addLast(lista_area, id) # Se agrega el id del vertice a la lista de vertices del cuadrante 4
                    
                else: # Si el mapa de areas no contiene el cuadrante 4
                    info = lt.newList('ARRAY_LIST') # Se crea una lista vacía para los vertices del cuadrante 4
                    lt.addLast(info, id) # Se agrega el id del vertice a la lista vacía
                    mp.put(data_structs["mapa_areas"], "a4", id) # Se agrega la pareja {llave: "a4", valor: lista de vertices} al mapa de areas
                    
                
            

        
        
            
        
    


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


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


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

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

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