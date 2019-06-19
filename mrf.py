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

## calculate pcc set with each count of measured nodes

if __name__ == "__main__":
    # 递归查找结构中的所有最大团 find all the maximum cliques
    cliques = cliqueSearch.CliqueSearch().searchCliques()
    
    pccRes = []

    # 生成测量节点 5- 60个 generate measuremenet node of range [5, 60]
    for i in range(5, 61):
        # 每种数量运算10中不同的测点 each type calculate 10 times
        for j in range(10):
            nodelist = {}
            # TODO 生成的sample应该是所有nodelist
            measureNodes = random.sample(range(1, 92), i)
            if excludeSupport:
                measureNodes = random.sample(range(1, 62), i)
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
                    # 采用测量数据 use measured value
                    nodelist[nodeNum] = {
                        'x': node['x'],
                        'y': node['y'],
                        'z': node['z'],
                        'value': node['value'],
                    }
                else:
                    # 采用随机数初始化 use init random value
                    nodelist[nodeNum] = {
                        'x': node['x'],
                        'y': node['y'],
                        'z': node['z'],
                        'value': rd[idx],
                    }
                idx += 1
            # print(measureNodes, end='\r\n')
            # print(json.dumps(nodelist, indent=1))

            # 迭代过程，遍历所有计算节点 iteration process
            for iterTick in range(4):
                for nodeNum, node in nodeMap.items():
                    if nodeNum in measureNodes:
                        continue
                    cliqueCalc.iterNode(nodeNum, cliques, nodelist)
            res = pd.DataFrame.from_dict(nodelist, orient='index')
            real = pd.DataFrame.from_dict(nodeMap, orient='index')
            data = pd.DataFrame()
            data['x'] = res['value']
            data['y'] = real['value']
            print(measureNodes, end='\r\n')
            # pccRes[i].append(pcc(data))
            pccRes.append({
                'num': i,
                'pcc': pcc(data)
            })
    print(json.dumps(pccRes, indent=1))
    resultFilename = 'res/res.csv'
    if excludeSupport:
        resultFilename = 'res/res_support.csv'
    pd.DataFrame(pccRes).to_csv(resultFilename)

    