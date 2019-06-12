import csv
import pandas as pd
import numpy as np
import random
import math

import json

from globalVariables import *
import cliqueSearch
import cliqueCalc
import node

## 变量找不到就去全局变量

def normalRandom(u1, u2, mean, var):
    return math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2) * math.sqrt(var) + mean

def mean(measureNodes):
    mean = 0
    for measureNode in measureNodes:
        mean += nodeMap[measureNode]['value']
    if len(measureNodes) > 0:
        mean = mean / len(measureNodes)
    return mean

def var(measureNodes):
    ave = mean(measureNodes)
    var = 0
    if (len(measureNodes) <= 1):
        return 0
    for measureNode in measureNodes:
        var += math.pow((nodeMap[measureNode]['value'] - ave), 2)
    var = var / (len(measureNodes) - 1)
    return var

def pcc(nodes):
    n = len(nodes)
    # print(valueSum)
    nodes['xy'] = nodes['x'] * nodes['y']
    nodes['xx'] = nodes['x'] * nodes['x']
    nodes['yy'] = nodes['y'] * nodes['y']
    valueSum = nodes.apply(sum)
    res = (n * valueSum['xy'] - valueSum['x'] * valueSum['y']) / (n * valueSum['xx'] - valueSum['x']**2)**0.5 / (n * valueSum['yy'] - valueSum['y']**2)**0.5
    return res

if __name__ == "__main__":
    # 递归查找结构中的所有最大团
    cliques = cliqueSearch.CliqueSearch().searchCliques()
    
    pccRes = []

    # 生成测量节点 5- 50个
    for i in range(5, 51):
        # 每种数量运算10中不同的测点
        for j in range(10):
            nodelist = {}
            # TODO 生成的sample应该是所有nodelist
            measureNodes = random.sample(range(1, 91), i)
            # 测量节点mean
            mu = mean(measureNodes)
            # 测量节点sigma
            sigma = math.sqrt(var(measureNodes))
            # 生成与节点数相同的正态随机数
            rd = np.random.normal(mu, sigma, len(nodeMap))
            # 初始化节点偏差
            idx = 0
            for nodeNum, node in nodeMap.items():
                if nodeNum in measureNodes:
                    # 采用测量数据
                    nodelist[nodeNum] = {
                        'x': node['x'],
                        'y': node['y'],
                        'z': node['z'],
                        'value': node['value'],
                    }
                else:
                    # 采用随机数初始化
                    nodelist[nodeNum] = {
                        'x': node['x'],
                        'y': node['y'],
                        'z': node['z'],
                        'value': rd[idx],
                    }
                idx += 1
            # print(measureNodes, end='\r\n')
            # print(json.dumps(nodelist, indent=1))

            # 迭代过程，遍历所有计算节点
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
    pd.DataFrame(pccRes).to_csv('res.csv')
            # print(real)
            # print(data)