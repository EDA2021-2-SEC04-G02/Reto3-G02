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


from DISClib.DataStructures.arraylist import iterator
import config as cf
import datetime as dt
import time
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
                'dateIndex': None,
                'cityIndex': None,
                'hourIndex': None,
                'longitudeIndex' : None
                }

    catalog['UFOS'] = lt.newList('SINGLE_LINKED', compareDates)
    catalog['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    catalog['cityIndex'] = mp.newMap(150,
                                    maptype='CHAINING',
                                    loadfactor=4.0,
                                    comparefunction=compareCities)
    catalog['hourIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareHours)
    catalog['longitudeIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareLongitude)
    return catalog

# Funciones para agregar informacion al catalogo

def addUFO(catalog, avistamiento):
    """
    """
    lt.addLast(catalog['UFOS'], avistamiento)
    updateDateIndex(catalog['dateIndex'], avistamiento)
    updateCityIndex(catalog['cityIndex'], avistamiento)
    updateHourIndex(catalog['hourIndex'], avistamiento)
    updateLongitudeIndex(catalog['longitudeIndex'], avistamiento)
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
    entry = mp.get(map, city)
    if entry is None:
        datentry = newCityEntry(city)
        mp.put(map, city, datentry)
    else:
        datentry = me.getValue(entry)
    addCityIndex(datentry, avistamiento)
    return map






def updateHourIndex(map, avistamiento):
    """
    Se toma la hora del avistamiento y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de avistamientos.
    Si no se encuentra creado un nodo para esa hora en el arbol
    se crea uno
    """
    occurredhour = avistamiento['datetime']
    UFOhour = dt.datetime.strptime(occurredhour, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, UFOhour.time())
    if entry is None:
        datentry = newDataEntry(UFOhour.time())
        om.put(map, UFOhour.time(), datentry)
    else:
        datentry = me.getValue(entry)
    addHourIndex(datentry, avistamiento)
    return map





def updateLongitudeIndex(map, avistamiento):
    """
    Se toma la longitud del avistamiento y se busca si ya existe en el arbol
    dicha longitud.  Si es asi, se adiciona a su lista de avistamientos.
    Si no se encuentra creado un nodo para esa longitud en el arbol
    se crea uno
    """
    longitude = round(float(avistamiento['longitude']),2)
    entry = om.get(map, longitude)
    if entry is None:
        datentry = newLongitudeEntry(longitude)
        om.put(map, longitude, datentry)
    else:
        datentry = me.getValue(entry)
    addLongitudeIndex(datentry, avistamiento)
    return map





def updateLatitudeIndex(map, avistamiento):
    """
    Se toma la latitud del avistamiento y se busca si ya existe en el arbol
    dicha latitud.  Si es asi, se adiciona a su lista de avistamientos.
    Si no se encuentra creado un nodo para esa latitud en el arbol
    se crea uno
    """
    latitude = round(float(avistamiento['latitude']),2)
    entry = om.get(map, latitude)
    if entry is None:
        datentry = newLatitudeEntry(latitude)
        om.put(map, latitude, datentry)
    else:
        datentry = me.getValue(entry)
    addLatitudeIndex(datentry, avistamiento)
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
    updateDateIndex(datentry['dateIndex'], avistamiento)
    return datentry




def addHourIndex(datentry, avistamiento):
    """
    Actualiza un indice.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es la hora y
    el valor es una lista con los avistamientos de dicho tipo en la hora que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstUFOS']
    lt.addLast(lst, avistamiento)
    return datentry




def addLongitudeIndex(datentry, avistamiento):
    """
    Actualiza un indice.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es la longitud y
    el valor es un mapa con la latitud como llave y valor los avistamientos de
    la longitud que se está consultando (dada por el nodo del arbol)
    """
    updateLatitudeIndex(datentry['latitudeIndex'], avistamiento)
    return datentry





def addLatitudeIndex(datentry, avistamiento):
    """
    Actualiza un indice.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es la latitud y
    el valor es una lista con los avistamientos de dicho tipo en la latitud que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstUFOS']
    lt.addLast(lst, avistamiento)
    return datentry




def newDataEntry(avistamiento):
    """
    Crea una entrada en el indice por fechas u horas, es decir en el arbol
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
    cityentry = {'city': None, 'dateIndex': None}
    cityentry['city'] = city
    cityentry['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return cityentry





def newLongitudeEntry(longitude):
    """
    Crea una entrada en el indice por ciudad, es decir en el arbol
    binario.
    """
    longitudentry = {'longitude': None, 'latitudeIndex': None}
    longitudentry['longitude'] = longitude
    longitudentry['latitudeIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareLatitude)
    return longitudentry




def newLatitudeEntry(latitude):
    """
    Crea una entrada en el indice por ciudad, es decir en el arbol
    binario.
    """
    latitudentry = {'latitude': None, 'lstUFOS': None}
    latitudentry['latitude'] = latitude
    latitudentry['lstUFOS'] = lt.newList('SINGLE_LINKED', compareDates)
    return latitudentry




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



def primerosAvistamientos(catalog, n):
    """
    Retrona los primeros n avistamientos
    """
    i = 0
    completa = False
    primerosUFOS = lt.newList()
    while lt.size(primerosUFOS) < n and not completa:
        UFOkey = om.select(catalog['dateIndex'],i)
        if UFOkey is None:
            completa = True
        else:
            UFO = om.get(catalog['dateIndex'], UFOkey)
            if UFO:
                lista = me.getValue(UFO)['lstUFOS']
                lista = ms.sort(lista,cmpUFOByDate)
                for a in lt.iterator(lista):
                    lt.addLast(primerosUFOS, a)
                    if lt.size(primerosUFOS) == n:
                        break
        i+=1
    return primerosUFOS


def ultimosAvistamientos(catalog, n):
    """
    Retrona los últimos n avistamientos
    """
    i = indexSize(catalog['dateIndex'])-1
    completa = False
    ultimosUFOS = lt.newList()
    while lt.size(ultimosUFOS) < n and not completa:
        UFOkey = om.select(catalog['dateIndex'],i)
        if UFOkey is None:
            completa = True
        else:
            UFO = om.get(catalog['dateIndex'], UFOkey)
            if UFO:
                lista = me.getValue(UFO)['lstUFOS']
                lista = ms.sort(lista, cmpUFOByDateInverso)
                for a in lt.iterator(lista):
                    lt.addFirst(ultimosUFOS, a)
                    if lt.size(ultimosUFOS) == n:
                        break
        i-=1
    return ultimosUFOS





def contarAvistamientosCiudad(catalog, ciudadIngresada):
    """
    Req 1: Cuenta los avistamientos de UFOS en una ciudad
    """
    tamanioCiudad = 0
    totalCiudades = mp.size(catalog['cityIndex'])
    TOPciudad = (None,0)
    for cityKey in lt.iterator(mp.keySet(catalog['cityIndex'])):
        city = mp.get(catalog['cityIndex'], cityKey)
        if city:
            city = (city,om.size(me.getValue(city)["dateIndex"]))
            if city[1] > TOPciudad[1]:
                TOPciudad = city
    
    ciudad = mp.get(catalog['cityIndex'], ciudadIngresada)
    if ciudad:
        ciudad = me.getValue(ciudad)
        primeros = primerosAvistamientos(ciudad, 3)
        ultimos = ultimosAvistamientos(ciudad, 3)
        tamanioCiudad = om.size(ciudad["dateIndex"])
    
    return totalCiudades, TOPciudad, tamanioCiudad, primeros, ultimos





def contarAvistamientosHora(catalog,horaInicial,minutoInicial,horaFinal,minutoFinal):
    """
    Req 3 (Individual): Cuenta los avistamientos en un rango de horas
    """
    timeMasTardeKey = om.maxKey(catalog["hourIndex"])
    timeMasTarde = om.get(catalog["hourIndex"],timeMasTardeKey)
    cantTimeMasTarde =lt.size(me.getValue(timeMasTarde)["lstUFOS"])
    
    timeInicial = dt.time(horaInicial,minutoInicial)
    timeFinal = dt.time(horaFinal,minutoFinal)
    llaveInicial = om.ceiling(catalog["hourIndex"], timeInicial)
    llaveFinal = om.floor(catalog["hourIndex"], timeFinal)
    avistamientos = om.values(catalog["hourIndex"],llaveInicial,llaveFinal)
    
    cantTotalUFOS = 0
    for UFO in lt.iterator(avistamientos):
        lista = UFO['lstUFOS']
        cantTotalUFOS += lt.size(lista)

    primerosUFOS = lt.newList()
    for UFO in lt.iterator(avistamientos):
        lista = UFO['lstUFOS']
        lista = ms.sort(lista,cmpUFOByDate)
        for a in lt.iterator(lista):
            lt.addLast(primerosUFOS, a)
            if lt.size(primerosUFOS) == 3:
                break
        if lt.size(primerosUFOS) == 3:
            break

    i = lt.size(avistamientos)
    completa = False
    ultimosUFOS = lt.newList()
    while lt.size(ultimosUFOS) < 3 and not completa:
        UFO = lt.getElement(avistamientos,i)['lstUFOS']
        if UFO:
            UFO = ms.sort(UFO, cmpUFOByDateInverso)
            for a in lt.iterator(UFO):
                lt.addFirst(ultimosUFOS, a)
                if lt.size(ultimosUFOS) == 3:
                    break
        else:
            completa = True
        i-=1

    return timeMasTardeKey, cantTimeMasTarde, cantTotalUFOS, primerosUFOS, ultimosUFOS






def contarAvistamientosDia(catalog,diaInicial,mesInicial,anioInicial,diaFinal,mesFinal,anioFinal):
    """
    Req 4: Cuenta los avistamientos en un rango de fechas
    """
    dateMasTardeKey = om.minKey(catalog["dateIndex"])
    dateMasTarde = om.get(catalog["dateIndex"],dateMasTardeKey)
    cantDateMasTarde =lt.size(me.getValue(dateMasTarde)["lstUFOS"])
    
    dateInicial = dt.date(anioInicial,mesInicial,diaInicial)
    dateFinal = dt.date(anioFinal,mesFinal,diaFinal)
    llaveInicial = om.ceiling(catalog["dateIndex"], dateInicial)
    llaveFinal = om.floor(catalog["dateIndex"], dateFinal)
    avistamientos = om.values(catalog["dateIndex"],llaveInicial,llaveFinal)
    
    cantTotalUFOS = 0
    for UFO in lt.iterator(avistamientos):
        lista = UFO['lstUFOS']
        cantTotalUFOS += lt.size(lista)

    primerosUFOS = lt.newList()
    for UFO in lt.iterator(avistamientos):
        lista = UFO['lstUFOS']
        lista = ms.sort(lista,cmpUFOByDate)
        for a in lt.iterator(lista):
            lt.addLast(primerosUFOS, a)
            if lt.size(primerosUFOS) == 3:
                break
        if lt.size(primerosUFOS) == 3:
            break

    i = lt.size(avistamientos)
    completa = False
    ultimosUFOS = lt.newList()
    while lt.size(ultimosUFOS) < 3 and not completa:
        UFO = lt.getElement(avistamientos,i)['lstUFOS']
        if UFO:
            UFO = ms.sort(UFO, cmpUFOByDateInverso)
            for a in lt.iterator(UFO):
                lt.addFirst(ultimosUFOS, a)
                if lt.size(ultimosUFOS) == 3:
                    break
        else:
            completa = True
        i-=1

    return dateMasTardeKey, cantDateMasTarde, cantTotalUFOS, primerosUFOS, ultimosUFOS







def contarAvistamientosZona(catalog,longInicial,latInicial,longFinal,latFinal):
    """
    Req 5: Cuenta los avistamientos en un rango de longitudes y latitudes
    """
    if longInicial >= longFinal:
        copia = longFinal
        longFinal = longInicial
        longInicial = copia
    llaveInicialLong = om.ceiling(catalog["longitudeIndex"], longInicial)
    llaveFinalLong = om.floor(catalog["longitudeIndex"], longFinal)
    if llaveInicialLong and llaveFinalLong:
        rangoLong = om.values(catalog["longitudeIndex"],llaveInicialLong,llaveFinalLong)
        
            








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
    city = me.getKey(city2)
    if (city1 == city):
        return 0
    elif (city1 > city):
        return 1
    else:
        return -1



def compareHours(hour1, hour2):
    """
    Compara dos horas
    """
    if (hour1 == hour2):
        return 0
    elif (hour1 > hour2):
        return 1
    else:
        return -1



def compareLongitude(lon1, lon2):
    """
    Compara dos longitudes
    """
    if (lon1 == lon2):
        return 0
    elif (lon1 > lon2):
        return 1
    else:
        return -1



def compareLatitude(lat1, lat2):
    """
    Compara dos latitudes
    """
    if (lat1 == lat2):
        return 0
    elif (lat1 > lat2):
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
