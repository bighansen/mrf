import csv
import pandas as pd
import numpy as np
import random
import math

import json

from globalVariables import *
from util import *
import cliqueSearch
import cliqueCalc

## calculate once with presented measured nodes

if __name__ == "__main__":
    # 递归查找结构中的所有最大团 find all the maximum cliques
    cliques = cliqueSearch.CliqueSearch().searchCliques()

    nodelist = {}
    measureNodes = [1,2,3,4,7,8,9,10,22,24,26,28,29,31,32,33,34,35,36,38,39,60,61]
    measureNodes.extend(range(62, 92))
    # average of measured
    mu = mean(measureNodes)
    # sigma of measured
    sigma = math.sqrt(var(measureNodes))
    # 生成与节点数相同的正态随机数 normal random numbers init
    rd = np.random.normal(mu, sigma, len(nodeMap))
    # 初始化节点偏差
    idx = 0
    for nodeNum, node in nodeMap.items():
        if nodeNum in measureNodes:
            # use measured value
            nodelist[nodeNum] = {
                'x': node['x'],
                'y': node['y'],
                'z': node['z'],
                'value': node['value'],
            }
        else:
            # use init random value
            nodelist[nodeNum] = {
                'x': node['x'],
                'y': node['y'],
                'z': node['z'],
                'value': rd[idx],
            }
        idx += 1
    data = pd.DataFrame()
    data['stochastic'] = pd.DataFrame.from_dict(nodelist, orient='index')['value']
    # 迭代过程，遍历所有计算节点 iteration process
    for iterTick in range(3):
        for nodeNum, node in nodeMap.items():
            if nodeNum in measureNodes:
                continue
            cliqueCalc.iterNode(nodeNum, cliques, nodelist)
    res = pd.DataFrame.from_dict(nodelist, orient='index')
    real = pd.DataFrame.from_dict(nodeMap, orient='index')
    data['x'] = res['value']
    data['y'] = real['value']
    print('pccvalue: {0}'.format(pcc(data)))
    pd.DataFrame(data).to_csv('res/res_single.csv')