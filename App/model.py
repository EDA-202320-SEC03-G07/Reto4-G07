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
    
    data_structs = {"comparendos": None,
                    "ditsancias": None,
                    "mapa_vertices": None,
                    "mapa_areas": None,
                    
                    "lat_max": float("-inf"),	
                    "lat_min": float("inf"),
                    "long_max": float("-inf"),
                    "long_min": float("inf"),
                    
                    "long_mid": 0,
                    "lat_mid": 0,
                    
        
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
    mapa_vertices = data_structs["mapa_vertices"]
    
    long_max = data_structs["long_max"]
    long_min = data_structs["long_min"]
    
    lat_max = data_structs["lat_max"]
    lat_min = data_structs["lat_min"]
    
    long_mid = data_structs["long_mid"]
    lat_mid = data_structs["lat_mid"]
    
    
    match archivo:
        case "bogota_vertices.txt":
            data = data.split(" ")
            id = data[0]
            longitud = data[1]
            latitud = data[2]
            vertice = {"long": longitud,
                       "lat": latitud,
                       "estacion": lt.newList("ARRAY_LIST"),
                       "comparendo": lt.newList("ARRAY_LIST"),
                       }
            mp.put(mapa_vertices, id, vertice)
            
            gr.insertVertex(data_structs["distancias"], id)
            gr.insertVertex(data_structs["comparendos"], id)
            
           
           
            if longitud > long_max:
                long_max = longitud
                
            if longitud < long_min:
                long_min = longitud 
                
            if latitud > lat_max:
                lat_max = latitud
                
            if latitud < lat_min:
                lat_min = latitud
             
             
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
            
            
            
            id_mas_cercano = None
            distancia_mas_cercano = float("inf")
            for vertice_id in lt.iterator(area_seleccionada):
                entrada = mp.get(mapa_vertices, vertice_id)
                vertice = me.getValue(entrada)
                distancia = haversine(data["EPOLATITUD"], data["EPOLONGITU"], vertice["lat"], vertice["long"])
                if distancia < distancia_mas_cercano:
                    distancia_mas_cercano = distancia
                    id_mas_cercano = vertice_id
            
            entrada = mp.get(mapa_vertices, id_mas_cercano)
            vertice = me.getValue(entrada)
            
            lista_estacion = vertice["estacion"]
            
            lt.addLast(lista_estacion, data)

                    
        
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
            
            
            
            id_mas_cercano = None
            distancia_mas_cercano = float("inf")
            for vertice_id in lt.iterator(area_seleccionada):
                entrada = mp.get(mapa_vertices, vertice_id)
                vertice = me.getValue(entrada)
                distancia = haversine(data["LATITUD"], data["LONGITUD"], vertice["lat"], vertice["long"])
                if distancia < distancia_mas_cercano:
                    distancia_mas_cercano = distancia
                    id_mas_cercano = vertice_id
            
            entrada = mp.get(mapa_vertices, id_mas_cercano)
            vertice = me.getValue(entrada)
            
            lista_estacion = vertice["estacion"]
            
            lt.addLast(lista_estacion, data)
            
            
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
    
    vertices = data_structs["mapa_vertices"]
    
    mapa_areas = data_structs["mapa_areas"]
    
    vertices_ids = mp.keySet(vertices)
    
    for id in lt.iterator(vertices_ids):
        entrada = mp.get(vertices, id)
        vertice = me.getValue(entrada)
        vertice_long = vertice["long"]
        vertice_lat = vertice["lat"]
        
        mitad_longitud = (data_structs["long_max"] - data_structs["long_min"]) / 2
        mitad_latitud = (data_structs["lat_max"] - data_structs["lat_min"]) / 2
        
        
        posicion = vertice_long >= mitad_longitud, vertice_lat >= mitad_latitud
        
        match posicion:
            
            case True, True:
       
                if mp.contains(mapa_areas, "a1"):
                    elemento = mp.get(mapa_areas, "a1")
                    lista_area = me.getValue(elemento)
                    lt.addLast(lista_area, id)
                        
                else:
                    info = lt.newList('ARRAY_LIST')
                    lt.addLast(info, id)
                    mp.put(mapa_areas, "a1", id)
            
            case False, True:
                
                if mp.contains(mapa_areas, "a2"):
                    elemento = mp.get(mapa_areas, "a2")
                    lista_area = me.getValue(elemento)
                    lt.addLast(lista_area, id)
                      
                else:
                    info = lt.newList('ARRAY_LIST')
                    lt.addLast(info, id)
                    mp.put(data_structs["mapa_areas"], "a2", id)
                    
            case False, False:
                
                if mp.contains(mapa_areas, "a3"):
                    elemento = mp.get(mapa_areas, "a3")
                    lista_area = me.getValue(elemento)
                    lt.addLast(lista_area, id)
                    
                else:
                    info = lt.newList('ARRAY_LIST')
                    lt.addLast(info, id)
                    mp.put(data_structs["mapa_areas"], "a3", id)
                    
            case True, False:
                
                if mp.contains(mapa_areas, "a4"):
                    elemento = mp.get(mapa_areas, "a4")
                    lista_area = me.getValue(elemento)
                    lt.addLast(lista_area, id)
                    
                else:
                    info = lt.newList('ARRAY_LIST')
                    lt.addLast(info, id)
                    mp.put(data_structs["mapa_areas"], "a4", id)
                    
                
            

        
        
            
        
    


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