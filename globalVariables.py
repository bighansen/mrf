import pandas as pd
import numpy as np
from collections import defaultdict

excludeSupport = True

# 原始坐标 raw theoretical node data
origins = pd.read_csv('data/data_nodes.csv', header=0, sep=',')
# 球心坐标 circle center
circle = [0,0,-1350]

# 计算节点对球心的方向向量 direction vectors
vectors = pd.DataFrame()
vectors['num'] = origins['num']
vectors['xn'] = origins['x'] - circle[0]
vectors['yn'] = origins['y'] - circle[1]
vectors['zn'] = origins['z'] - circle[2]
vectors['length'] = np.sqrt(vectors['xn']**2 + vectors['yn']**2 + vectors['zn']**2)
vectors['xn'] /= vectors['length'] 
vectors['yn'] /= vectors['length']
vectors['zn'] /= vectors['length']

# 计算三维坐标形式的节点偏移量 nodal coordinate diffs
_data_measure_filename = 'data/data_measure.csv'
measures = pd.read_csv(_data_measure_filename, header=0, sep=',')
diffXYZs = pd.DataFrame()
diffXYZs['x'] = measures['x'] - origins['x']
diffXYZs['y'] = measures['y'] - origins['y']
diffXYZs['z'] = measures['z'] - origins['z']

# 计算径向偏移 diffs along radius
diffs = pd.DataFrame()
diffs['num'] = vectors['num']
diffs['x'] = origins['x']
diffs['y'] = origins['y']
diffs['z'] = origins['z']
diffs['value'] = diffXYZs['x'] * vectors['xn'] + diffXYZs['y'] * vectors['yn'] + diffXYZs['z'] * vectors['zn']
#为了方便node查找存成dict
nodeMap = {}
for idx, diff in diffs.iterrows():
    nodeMap[int(diff['num'])] = {
        'x': diff['x'],
        'y': diff['y'],
        'z': diff['z'],
        'value': diff['value']
    }

# 存储每个点的所有相邻点 find neighbors nodes of each node
edges = pd.read_csv('data/data_elements.csv', header=0, sep=',')
neighbors = defaultdict(list)
for index, edge in edges.iterrows():
    neighbors[int(edge['vi'])].append(int(edge['vj']))
    neighbors[int(edge['vj'])].append(int(edge['vi']))