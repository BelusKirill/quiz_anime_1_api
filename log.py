from datetime import datetime

def add_log(message, namedef):
    with open('log.log', 'a') as f:
        message = f'{message}\nnamedef: {namedef}\ntime: {datetime.now()}\n\n'
        f.write(message)
        print(message)