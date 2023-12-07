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
 """
 
import config as cf
import model
import time
import tracemalloc
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    
    return model.new_data_structs()


# ====================================================================================================================================================================== #
# =========================================================================== Carga de Datos =========================================================================== #
# ====================================================================================================================================================================== #


def load_data(data_structs):
    """
    Carga los datos del reto
    """
    
    vertices_archivo = cf.data_dir + 'bogota_vertices.txt' # Se crea el camino al archivo de vertices
    with open(vertices_archivo, 'r') as f: # Se abre el archivo de vertices
        vertices = f.readlines()
    for vertice in vertices:
        model.add_data(data_structs, 'bogota_vertices.txt', vertice)
    
    
    estaciones_archivo = cf.data_dir + 'estacionpolicia_bogota_vertices.csv' # Se crea el camino al archivo de estaciones
    f = open(estaciones_archivo, 'r', encoding='utf-8') # Se abre el archivo de estaciones
    estaciones = csv.DictReader(f) # Se formatea el archivo de estaciones en diccionarios
    for estacion in estaciones:
        model.add_data(data_structs, 'estacionpolicia_bogota_vertices.csv', estacion)
    model.insert_vertex_estaciones(data_structs)  
        
    comparendos_archivo = cf.data_dir + 'comparendos_2019_bogota_vertices.csv' # Se crea el camino al archivo de comparendos
    f = open(comparendos_archivo, 'r', encoding='utf-8') # Se abre el archivo de comparendos
    comparendos = csv.DictReader(f) # Se formatea el archivo de comparendos en diccionarios
    for comparendo in comparendos:
        model.add_data(data_structs, 'comparendos_2019_bogota_vertices.csv', comparendo)
    model.max_pq_localidades_comparendos(data_structs)
    model.max_pq_vehiculo_comparendos(data_structs)
    model.max_pq_gravedad_comparendos(data_structs)

    arcos_archivo = cf.data_dir + 'bogota_arcos.txt' # Se crea el camino al archivo de arcos
    with open(arcos_archivo, 'r') as f: # Se abre el archivo de arcos
        arcos = f.readlines()
    for arco in arcos:
        model.add_data(data_structs, 'bogota_arcos.txt', arco)


# ====================================================================================================================================================================== #
# ==================================================================== Reslución de Requerimientos ===================================================================== #
# ====================================================================================================================================================================== #


def req_1(control, latitud_vertice_origen, longitud_vertice_origen, latitud_vertice_destino, longitud_vertice_destino):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    
    dt1 = get_time()
    dm1 = get_memory()
    
    total_vertices, total_distancia, pathTo = model.req_1(control, latitud_vertice_origen, longitud_vertice_origen, latitud_vertice_destino, longitud_vertice_destino)
    
    dt2 = get_time()
    dm2 = get_memory()
    dt = delta_time(dt1,dt2)
    dm = abs(delta_memory(dm1,dm2))
    
    return total_vertices, total_distancia, pathTo, dt, dm


def req_2(data_structs, latitud_vertice_origen, longitud_vertice_origen, latitud_vertice_destino, longitud_vertice_destino):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    
    dt1 = get_time()
    dm1 = get_memory()
    
    total_vertices, total_distancia, pathTo = model.req_2(data_structs, latitud_vertice_origen, longitud_vertice_origen, latitud_vertice_destino, longitud_vertice_destino)
    
    dt2 = get_time()
    dm2 = get_memory()
    dt = delta_time(dt1,dt2)
    dm = abs(delta_memory(dm1,dm2))
    
    return total_vertices, total_distancia, pathTo, dt, dm


def req_3(control, consulta_camaras, consulta_localidad):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    
    dt1 = get_time()
    dm1 = get_memory()
    total_camaras, id_vertices, arcos, extension, costo = model.req_3(control, consulta_camaras, consulta_localidad)
    dt2 = get_time()
    dm2 = get_memory()
    dt = delta_time(dt1,dt2)
    dm = abs(delta_memory(dm1,dm2))
    return total_camaras, id_vertices, arcos, extension, costo, dt, dm


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    total_camara, id_vertices, arcos, extension, costo = model.req_4(control)
    return total_camara, id_vertices, arcos, extension, costo


def req_5(control, consulta_camaras, consulta_clase_vehiculo):
    """
    Retorna el resultado del requerimiento 5
    """
    # try:
    t0 = get_time()
    m0 = get_memory()
    total_camaras, id_vertices, arcos, extension, costo = model.req_5(control, consulta_camaras, consulta_clase_vehiculo)
    t1 = get_time()
    m1 = get_memory()
    
    dt = delta_time(t0,t1)
    dm = abs(delta_memory(m0,m1))
    return total_camaras, id_vertices, arcos, extension, costo, dt, dm


def req_6(control, num_comparendos_graves):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    t0 = get_time()
    m0 = get_memory()
    lista = model.req_6(control, num_comparendos_graves)
    t1 = get_time()
    m1 = get_memory()
    
    dt = delta_time(t0,t1)
    dm = abs(delta_memory(m0,m1))
    
    return lista, dt, dm
    

def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# ====================================================================================================================================================================== #
# ============================================================= Funciones para medir tiempos de ejecucion ============================================================== #
# ====================================================================================================================================================================== #


def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return round(elapsed,2)

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    tracemalloc.start()
    return tracemalloc.take_snapshot()

def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
