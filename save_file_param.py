# json файл для сохранения параметров для модели

import os.path
import json
def save_json(name, data, method='replace'):
    file_name = 'to_model/parametres.json'
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            file = {'names': 'datas'}
            json.dump(file, f)
    with open(file_name, 'r+') as f:
        file = json.load(f)
        if method == 'replace':
            file[name] = data
        elif method == 'append':
            file[name] += data
    with open(file_name, 'r+') as f:
        json.dump(file, f)
    return 'Записано'

def open_json():
    file_name = 'parametres.json'
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            file = json.load(f)
        return file
    else:
        return 'нет такого файла'
