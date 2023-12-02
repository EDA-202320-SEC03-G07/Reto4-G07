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
                   
                    
        
                    }
    
    
    data_structs["comparendos"] = gr.newGraph(datastructure="ADJ_LIST", directed=False)
    
    data_structs["distancias"] = gr.newGraph(datastructure="ADJ_LIST", directed=False)
    
    data_structs["mapa_vertices"] = mp.newMap(numelements=228045, maptype="PROBING", loadfactor=0.5)
    
    
    
    return data_structs
    


# Funciones para agregar informacion al modelo

def add_data(data_structs, archivo, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    mapa_vertices = data_structs["mapa_vertices"] # Mapa: {id: vertice}
    
    
    
    match archivo:
        case "bogota_vertices.txt": # Se agrega un vertice al mapa de vertices
            data = data.split(',') # Se formatea la información de string "# # #" a lista ["#", "#", "#"]
            id = data[0] # Se obtiene el id del vertice en la primera posición de la lista
            longitud = float(data[1]) # Se obtiene la longitud del vertice en la segunda posición de la lista
            latitud = float(data[2]) # Se obtiene la latitud del vertice en la tercera posición de la lista
            
            
            # Se crea un vertice con la información obtenida en formato dict
            vertice = {"long": longitud, 
                       "lat": latitud,
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
                      
            vertice_mas_cercano = data["VERTICES"]
            if mp.contains(mapa_vertices, vertice_mas_cercano):
                entrada_vertice =  mp.get(mapa_vertices, vertice_mas_cercano)
                vertice = me.getValue(entrada_vertice)
                lt.addLast(vertice["comparendos"], data)
                    
                
                
                           
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