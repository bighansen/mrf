from globalVariables import *
from util import *

import pandas as pd
import numpy as np
import json
import random
import math

if __name__ == "__main__":
    pccRes = []

    # 生成测量节点 5- 50个
    for i in range(5, 61):
        # 每种数量运算10中不同的测点
        for j in range(10):
            nodelist = {}
            # TODO 生成的sample应该是所有nodelist
            measureNodes = random.sample(range(1, 91), i)
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
    resultFilename = 'res/stochastic_res.csv'
    if excludeSupport:
        resultFilename = 'res/stochastic_res_support.csv'
    pd.DataFrame(pccRes).to_csv(resultFilename)