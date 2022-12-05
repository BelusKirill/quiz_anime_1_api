from configparser import ConfigParser

def getData(section, param, ttype=str, filename='data.ini'):
    parser = ConfigParser()
    parser.read(filename)

    return ttype(parser[section][param])