
# coding: utf-8

import csv
import os
import sys
import numpy as np
import pandas as pd
import time

def counter(file_name,dT=0.3):
    dT=float(dT)
    df = pd.read_csv(file_name)
    M = df.feature1.max()+1 #считываем число  M (возможных значений фич)
    array = df.sort_values('time').values #сортировка по времени инцидента
    Result = {} #дикт с результатом, можно сразу записать в файл
    box = np.empty((M,M), dtype=object) # матрица записей времени срабатывания инцидентов с одинаковыми фичами
    box.fill([])
    for i in (range(0,len(array))):
        feature1 =  int(array[i][1])
        feature2 =  int(array[i][2])
        time_border = array[i][3] - dT #граница времени, по которой отрезаем инциденты
        time_counts = ((box[feature1,feature2]-time_border)>0).sum() #считаем инциденты, попавшие в границы времени
        box[feature1,feature2] = np.append(box[feature1,feature2],(array[i][3])) #докладываем время текущего инцидента в ячейку
        Result[int(array[i][0])]=time_counts
    with open('results.csv', 'w') as f:  # Just use 'w' mode in 3.x
        fieldnames = ['id', 'counts']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        data = [dict(zip(fieldnames, [k, v])) for k, v in Result.items()]
        writer.writerows(data)

if __name__ == '__main__':
    file_name = os.path.basename(sys.argv[1])
    if len(sys.argv)==3:
        dT = os.path.basename(sys.argv[2])
    else: dT=0.3
    startTime = time.time()
    counter(file_name,dT)
    elapsedTime = time.time() - startTime
    print('function [{}] finished in {} s'.format('incidents_counter', int(elapsedTime)))

