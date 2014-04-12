__author__ = 'benoit'

import yaml
try:
    import yaml.CLoader as Loader
except ImportError:
    import yaml.Loader as Loader

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
    if resdata:
        filename = resdata.get('image', None)

    if not filename:
        raise ResourceNotFoundError(resname)

def getValue(resname):
    """
    Return the value for the name provided
    """
    (obj,val) = resname.split('.')
    return getObj(obj)[val]
