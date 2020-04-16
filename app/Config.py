# ==========================================
#
# Pygame Arkanoid
# Autor: manuel.mayo.lado@gmail.com
#
# ==========================================

import os
from collections import namedtuple

"""
En este módulo cargamos la configuración del juego en la variable <config>,
que usaremos en toda la aplicación.
"""

def load_config_file(file_name='config.conf'):
    """
    Devuelve la configuración del juego del archivo especificado

    @args 
        file (optional): str. Archivo de configuración

    @return 
        dict
    """
    config_dict = {}
    key = 'unknown'

    for line in load_file(file_name):
        line = line.strip()
        if line:
            config_line = load_line(line)
            if 'key' in config_line:
                key = config_line['key']
                config_dict[key] = {}
            elif 'subkey' in config_line:
                subkey = config_line['subkey']
                value = config_line['value']
                config_dict[key][subkey] = value
    return config_dict


def load_file(file_name):
    """
    Devuelve una lista con las lineas de texto del archivo especificado

    @args 
        file: str. Archivo de configuración

    @return 
        list
    """
    config_file_text = ''

    if os.path.exists(file_name):
        config_file = open(file_name)
        config_file_text = config_file.read()

    return config_file_text.split('\n')


def load_line(line):
    """
    Devuelve la información de una linea del archivo de configuración del juego

    @args 
        line: str. Línea de texto

    @return 
        dict
    """
    if line[0]+line[-1] == "[]":
        return {'key': line.strip("[]")}
    else:
        if len(line.split(':')) >= 2:
            subkey, value = [l.strip() for l in line.split(':')][:2]
            if value.isnumeric():
                v = int(value)
            else:
                try:
                    v = float(value)
                except:
                    v = value.strip()
            return {'subkey': subkey, 'value': v}


def generate_config_object(datadict):
    """
    Genera un objeto a partir de un diccionario

    @args
        datadict: dict.

    @return
        object Struct
    """
    return namedtuple('Struct', datadict.keys()) (
        *[namedtuple('Struct', x.keys())(*x.values()) for x in datadict.values()]
    )

# Variables con la onfiguración del juego

config_dict = load_config_file()

config = generate_config_object(config_dict)