
import numpy as np
import pandas as pd
import dill
from tqdm import tqdm
import os, sys
import statistics
from scipy.stats import iqr
import json
from datetime import datetime, date 
import time

from other.save_file_param import open_json
param_json = open_json()

from sklearn.metrics import f1_score
import mysql.connector




def predict_megafon():
    with open('other/models/model_dill.pkl', 'rb') as f:
        model = dill.load(f)

    data_test = pd.read_csv('data_test.csv')
    dict_w = list(data_test['id'].unique())
    con = mysql.connector.connect(host='localhost', user='web_user', password='1111', db='megafon')
    sql = f"select * from features where id in {dict_w}"
    data_features = pd.read_sql(sql, con)
    if data_features.shape[0] == 0:
        return 'Нет такого пользователя'
    data_features.drop('index', axis=1, inplace=True)

    data = pd.merge_asof(data_test, data_features, on='buy_time', by='id', direction='nearest')
    y_pred = model.predict_proba(data)[:,1][0]
    if y_pred >= param_json['xgb_pca']:
        pred = 1
    else:
        pred = 0
    
    from megafon.predict_megafon import predict_megafon
    out = predict_megafon(data, param_json, model)
    out = [int(i) for i in out.loc[0][1:]]

    model = None
    return jsonify({0: f'{pred}/{int(round(y_pred, 2)*100)}%', 1: out[0], 2: out})

predict_megafon()