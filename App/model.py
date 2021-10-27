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
import datetime as dt
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """ Inicializa el analizador
    Crea una lista vacia para guardar todos los avistamientos
    Se crean indices (Maps) por los siguientes criterios:
    -Datetime
    Retorna el analizador inicializado.
    """
    catalog = {'UFOS': None,
                'dateIndex': None
                }

    catalog['UFOS'] = lt.newList('SINGLE_LINKED', compareDates)
    catalog['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    catalog['cityIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareCities)
    return catalog

# Funciones para agregar informacion al catalogo

def addUFO(catalog, avistamiento):
    """
    """
    lt.addLast(catalog['UFOS'], avistamiento)
    updateDateIndex(catalog['dateIndex'], avistamiento)
    updateCityIndex(catalog['cityIndex'], avistamiento)
    return catalog



def updateDateIndex(map, avistamiento):
    """
    Se toma la fecha del avistamiento y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de avistamientos.
    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea uno
    """
    occurreddate = avistamiento['datetime']
    UFOdate = dt.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, UFOdate.date())
    if entry is None:
        datentry = newDataEntry(UFOdate.date())
        om.put(map, UFOdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, avistamiento)
    return map




def updateCityIndex(map, avistamiento):
    """
    Se toma la ciudad del avistamiento y se busca si ya existe en el arbol
    dicha ciudad.  Si es asi, se adiciona a su lista de avistamientos.
    Si no se encuentra creado un nodo para esa ciudad en el arbol
    se crea uno
    """
    city = avistamiento['city']
    entry = om.get(map, city)
    if entry is None:
        datentry = newCityEntry(city)
        om.put(map, city, datentry)
    else:
        datentry = me.getValue(entry)
    addCityIndex(datentry, avistamiento)
    return map




def addDateIndex(datentry, avistamiento):
    """
    Actualiza un indice.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es la fecha y
    el valor es una lista con los avistamientos de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstUFOS']
    lt.addLast(lst, avistamiento)
    return datentry




def addCityIndex(datentry, avistamiento):
    """
    Actualiza un indice.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es la fecha y
    el valor es una lista con los avistamientos de dicho tipo en la ciudad que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstCity']
    lt.addLast(lst, avistamiento)
    return datentry





def newDataEntry(avistamiento):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'name': None, 'lstUFOS': None}
    entry['name'] = avistamiento
    entry['lstUFOS'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry




def newCityEntry(city):
    """
    Crea una entrada en el indice por ciudad, es decir en el arbol
    binario.
    """
    cityentry = {'city': None, 'lstCity': None}
    cityentry['city'] = city
    cityentry['lstCity'] = lt.newList('SINGLELINKED', compareCities)
    return cityentry




# Funciones para creacion de datos

# Funciones de consulta

def avistamientosSize(catalog):
    """
    Numero de avistamientos leidos
    """
    return lt.size(catalog['UFOS'])



def indexHeight(catalog):
    """
    Altura del arbol
    """
    return om.height(catalog)


def indexSize(catalog):
    """
    Numero de elementos en el indice
    """
    return om.size(catalog)



def primerosAvistamientos(catalog):
    """
    Retrona los primeros 5 avistamientos
    """
    i = 0
    primerosUFOS = lt.newList()
    while lt.size(primerosUFOS) < 5:
        UFOkey = om.select(catalog['dateIndex'],i)
        UFO = om.get(catalog['dateIndex'], UFOkey)
        if UFO:
            lista = me.getValue(UFO)['lstUFOS']
            lista = ms.sort(lista,cmpUFOByDate)
            for a in lt.iterator(lista):
                lt.addLast(primerosUFOS, a)
                if lt.size(primerosUFOS) == 5:
                    break
        i+=1
    return primerosUFOS


def ultimosAvistamientos(catalog):
    """
    Retrona los últimos 5 avistamientos
    """
    i = indexSize(catalog['dateIndex'])-1
    ultimosUFOS = lt.newList()
    while lt.size(ultimosUFOS) < 5:
        UFOkey = om.select(catalog['dateIndex'],i)
        UFO = om.get(catalog['dateIndex'], UFOkey)
        if UFO:
            lista = me.getValue(UFO)['lstUFOS']
            lista = ms.sort(lista, cmpUFOByDateInverso)
            for a in lt.iterator(lista):
                lt.addFirst(ultimosUFOS, a)
                if lt.size(ultimosUFOS) == 5:
                    break
        i-=1
    return ultimosUFOS





def contarAvistamientosCiudad(catalog, ciudadIngresada):
    """
    Req 1: Cuenta los avistamientos de UFOS en una ciudad
    """
    tamanioCiudad = 0
    totalCiudades = om.size(catalog['cityIndex'])
    lstCiudades = lt.newList()
    for cityKey in lt.iterator(om.keySet(catalog['cityIndex'])):
        city = om.get(catalog['cityIndex'], cityKey)
        if city:
            lt.addLast(lstCiudades, (city,lt.size(me.getValue(city)["lstCity"])))
    ordenada = ms.sort(lstCiudades,cmpCities)
    TOP5ciudades = lt.subList(ordenada,1,5)
    ciudad = om.get(catalog['cityIndex'], ciudadIngresada)
    if ciudad:
        ciudad = me.getValue(city)
        tamanioCiudad = lt.size(ciudad["lstCity"])

    return 0





# Funciones utilizadas para comparar elementos dentro de una lista

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareUFOS(UFO1, UFO2):
    """
    Compara dos tipos de UFOS
    """
    UFO = me.getKey(UFO2)
    if (UFO1 == UFO):
        return 0
    elif (UFO1 > UFO):
        return 1
    else:
        return -1



def compareCities(city1, city2):
    """
    Compara dos ciudades
    """
    city = city2
    if (city1 == city):
        return 0
    elif (city1 > city):
        return 1
    else:
        return -1



def cmpUFOByDate(UFO1, UFO2):
    """
    Se obtiene verdadero si el UFO1 ocurre antes del UFO2
    """
    return UFO1["datetime"]<UFO2["datetime"]


def cmpUFOByDateInverso(UFO1, UFO2):
    """
    Se obtiene verdadero si el UFO1 ocurre después del UFO2
    """
    return UFO1["datetime"]>UFO2["datetime"]



def cmpCities(city1, city2):
    """
    Se obtiene verdadero si city 1 tiene más avistamientos que city2
    """
    return city1[1]>city2[1]

# Funciones de ordenamiento
