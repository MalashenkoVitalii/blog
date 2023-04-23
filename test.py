import logging
logging.basicConfig(filename='logs.log', level=logging.DEBUG)

a = 25
try:
    print(a+'str')
except TypeError:
    print('TypeError')
    logging.info('TypeError')
    logging.error('Error')
    logging.warning('Warning')
