# generate anays node files mrf

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

if __name__ == "__main__":
    # 递归查找结构中的所有最大团
    cliques = cliqueSearch.CliqueSearch().searchCliques()
    
    pccRes = []

    # 生成测量节点 5- 60个
    for i in range(5, 61):
        # 每种数量运算10中不同的测点
        for j in range(10):
            nodelist = {}
            # TODO 生成的sample应该是所有nodelist
            measureNodes = random.sample(range(1, 92), i)
            if excludeSupport:
                measureNodes = random.sample(range(1, 62), i)
                measureNodes.extend(range(62, 92))
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
            res.index = range(0, len(res))
            # originRes = pd.DataFrame.from_dict(originMap, orient='index')
            nodeRes = pd.DataFrame()
            nodeRes['!node'] = ['k'] * 91
            nodeRes['num'] = vectors['num']
            nodeRes['x'] = (res['value'] * vectors['xn'] + res['x']) / 1000
            nodeRes['y'] = (res['value'] * vectors['yn'] + res['y']) / 1000
            nodeRes['z'] = (res['value'] * vectors['zn'] + res['z']) / 1000
            nodeRes.to_csv(f'res/nodes/node_{i}_{j}.txt', index=None)