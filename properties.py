from jproperties import Properties


###############
#  CONSTANTS  #
###############

_CONFIG = Properties()


###############
#  FUNCTIONS  #
###############

def exists(key):
    return _CONFIG.get(key) is not None

def get(key):
    return _CONFIG.get(key).data


############
#  SCRIPT  #
############

with open("code.properties", 'rb') as config_file:
    _CONFIG.load(config_file)
