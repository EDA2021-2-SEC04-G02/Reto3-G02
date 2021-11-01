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
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newCatalog()
    return analyzer


# Funciones para la carga de datos


def cargarData(catalog):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    UFOSfile = cf.data_dir + 'UFOS-utf8-small.csv'
    input_file = csv.DictReader(open(UFOSfile, encoding='utf-8'),
                                delimiter=",")
    for avistamiento in input_file:
        model.addUFO(catalog, avistamiento)
    return catalog

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


def avistamientosSize(catalog):
    """
    Numero de avistamientos leidos
    """
    return model.avistamientosSize(catalog)


def indexHeight(catalog):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(catalog)


def indexSize(catalog):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(catalog)



def primerosAvistamientos(catalog, n):
    """
    Retrona los primeros n avistamientos
    """
    return model.primerosAvistamientos(catalog, n)


def ultimosAvistamientos(catalog, n):
    """
    Retrona los últimos n avistamientos
    """
    return model.ultimosAvistamientos(catalog, n)



def contarAvistamientosCiudad(catalog, ciudad):
    """
    Cuenta los avistamientos de UFOS en una ciudad
    """
    result = model.contarAvistamientosCiudad(catalog, ciudad)
    return result




def contarAvistamientosHora(catalog,horaInicial,minutoInicial,horaFinal,minutoFinal):
    """
    Cuenta los avistamientos en un rango de horas
    """
    result = model.contarAvistamientosHora(catalog,horaInicial,minutoInicial,horaFinal,minutoFinal)
    return result




def contarAvistamientosDia(catalog,diaInicial,mesInicial,anioInicial,diaFinal,mesFinal,anioFinal):
    """
    Cuenta los avistamientos en un rango de fechas
    """
    result = model.contarAvistamientosDia(catalog,diaInicial,mesInicial,anioInicial,diaFinal,mesFinal,anioFinal)
    return result





def contarAvistamientosZona(catalog,longInicial,latInicial,longFinal,latFinal):
    """
    Cuenta los avistamientos en un rango de longitudes y latitudes
    """
    result = model.contarAvistamientosZona(catalog,longInicial,latInicial,longFinal,latFinal)
    return result
