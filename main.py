import csv
import pandas as pd
import numpy as np
from collections import defaultdict
import random

origins = pd.read_csv('data_nodes.csv', header=0, sep=',')

# 球心坐标
circle = [0,0,-1350]

# 计算节点对球心的方向向量
vectors = pd.DataFrame()
vectors['num'] = origins['num']
vectors['xn'] = origins['x'] - circle[0]
vectors['yn'] = origins['y'] - circle[1]
vectors['zn'] = origins['z'] - circle[2]
vectors['length'] = np.sqrt(vectors['xn']**2 + vectors['yn']**2 + vectors['zn']**2)
vectors['xn'] /= vectors['length'] 
vectors['yn'] /= vectors['length']
vectors['zn'] /= vectors['length']

# 计算三维坐标形式的节点偏移量
measures = pd.read_csv('data_measure.csv', header=0, sep=',')
diffXYZs = pd.DataFrame()
diffXYZs['x'] = measures['x'] - origins['x']
diffXYZs['y'] = measures['y'] - origins['y']
diffXYZs['z'] = measures['z'] - origins['z']

# 计算径向偏移
diffs = pd.DataFrame()
diffs['num'] = vectors['num']
diffs['originX'] = origins['x']
diffs['originY'] = origins['y']
diffs['originZ'] = origins['z']
diffs['p'] = diffXYZs['x'] * vectors['xn'] + diffXYZs['y'] * vectors['yn'] + diffXYZs['z'] * vectors['zn']

# 存储每个点的所有相邻点
edges = pd.read_csv('data_elements.csv', header=0, sep=',')
neighbors = defaultdict(list)
for index, edge in edges.iterrows():
    neighbors[int(edge['vi'])].append(int(edge['vj']))
    neighbors[int(edge['vj'])].append(int(edge['vi']))


cliquesHash = {}    # 存储最大团的hash
cliquesNotMax = {}  # 由于算法存在伪最大团，将算法中间过程的团存储在这里，最后filter
def findNeighbors(nodes: list):
    res = []
    for node in nodes:
        nodeNeighbor = neighbors[node]
        res.extend(nodeNeighbor)
    res = list(set(res))
    for node in nodes:
        if node in res:
            res.remove(node)
    return res

def myhash(nodes: list):
    res = 0
    for node in nodes:
        res += node**2
    res = np.sqrt(res)/len(nodes)
    return res

def generateCliques(nodes: list, groups: list):
    # 查找节点组的全部相邻节点
    nodeNeighbors = findNeighbors(nodes)
    # 每个相邻节点判断是否与所有nodes中的节点相邻
    for neighbor in nodeNeighbors:
        isNeignbor = True
        for node in nodes:
            if neighbor not in neighbors[node]:
                # 临近点不是团节点，则去重后添加当前的节点团
                # TODO 去掉重复clique
                if myhash(nodes) not in cliquesHash.keys():
                    groups.append(nodes)
                    cliquesHash[myhash(nodes)] = nodes
                isNeignbor = False
                break
        if isNeignbor:
            cliquesNotMax[myhash(nodes)] = nodes
            newNodes = nodes.copy()
            newNodes.append(neighbor)
            generateCliques(newNodes, groups)


# 遍历节点, 生成cliques
cliques = []
for index, node in origins.iterrows():
    # 寻找节点的相邻点
    generateCliques([node['num']], cliques)
cliques = list(filter(lambda x: myhash(x) not in cliquesNotMax.keys(), cliques))

def normalRandom():
    pass

# 生成测量节点 5- 50个
for i in range(5,50):
    # 每种数量运算10次
    for j in range(1,10):
        nodelist = {}
        measureNodes = random.sample(range(1, 91), i)
        for idx, diff in diffs.iterrows():
            if diff['num'] in measureNodes:
                # 采用测量数据
                nodelist[int(diff['num'])] = {
                    x: diff['originX'],
                    y: diff['originY'],
                    z: diff['originZ'],
                    value: diff['p'],
                }
            else:
                # 采用随机数初始化
                nodelist[int(diff['num'])] = {
                    x: diff['originX'],
                    y: diff['originY'],
                    z: diff['originZ'],
                    value: normalRandom(),
                }
                pass