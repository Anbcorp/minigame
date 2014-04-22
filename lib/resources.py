__author__ = 'benoit'

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader as Loader

data = yaml.load(open('resources.yaml'), Loader=Loader)

class ResourceNotFoundError(Exception):
    def __init__(self, resname):
        message = "Didn't find entry for %s" % (resname)
        super(ResourceNotFoundError, self).__init__(message)

def getImage(resname):
    """
    Return the filename corresponding to the resource name provided
    """
    resdata = data.get(resname, None)
    filename = None
    if resdata:
        filename = resdata.get('image', None)

    if not filename:
        raise ResourceNotFoundError(resname)

    return filename

def getObject(object_name):
    try :
        object_data = data[object_name]
    except KeyError, ke :
        raise ResourceNotFoundError(object_name)

    return object_data

def getValue(resource):
    """
    Return the value for the name provided
    """
    (object_name, value_name) = resource.split('.')

    object_data = getObject(object_name)
    try :
        value = object_data[value_name]
    except KeyError, kerror:
        raise ResourceNotFoundError(resource)

    return value

if __name__ == '__main__':
    print getImage('player')
    print getValue('player.start')
    print getValue('player.speed')
