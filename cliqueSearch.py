from globalVariables import *
import pandas as pd
import numpy as np

class CliqueSearch:
    def __init__(self):
        self._cliquesHash = {}    # 存储最大团的hash
        self._cliquesNotMax = {}  # 由于算法存在伪最大团，将算法中间过程的团存储在这里，最后filter

    def _findNeighbors(self, nodes: list):
        res = []
        for node in nodes:
            nodeNeighbor = neighbors[node]
            res.extend(nodeNeighbor)
        res = list(set(res))
        for node in nodes:
            if node in res:
                res.remove(node)
        return res

    def _myhash(self, nodes: list):
        res = 0
        for node in nodes:
            res += node**2
        res = np.sqrt(res)/len(nodes)
        return res

    def _generateCliques(self, nodes: list, groups: list):
        # 查找节点组的全部相邻节点
        nodeNeighbors = self._findNeighbors(nodes)
        # 每个相邻节点判断是否与所有nodes中的节点相邻
        for neighbor in nodeNeighbors:
            isNeignbor = True
            for node in nodes:
                if neighbor not in neighbors[node]:
                    # 临近点不是团节点，则去重后添加当前的节点团
                    # TODO 去掉重复clique
                    if self._myhash(nodes) not in self._cliquesHash.keys():
                        groups.append(nodes)
                        self._cliquesHash[self._myhash(nodes)] = nodes
                    isNeignbor = False
                    break
            if isNeignbor:
                self._cliquesNotMax[self._myhash(nodes)] = nodes
                newNodes = nodes.copy()
                newNodes.append(neighbor)
                self._generateCliques(newNodes, groups)

    # 遍历节点, 生成cliques
    def searchCliques(self):
        cliques = []
        self._cliquesHash = {}    # 存储最大团的hash
        self._cliquesNotMax = {}  # 由于算法存在伪最大团，将算法中间过程的团存储在这里，最后filter
        for index, node in origins.iterrows():
            # 寻找节点的相邻点
            self._generateCliques([node['num']], cliques)
        cliques = list(filter(lambda x: self._myhash(x) not in self._cliquesNotMax.keys(), cliques))
        return cliques