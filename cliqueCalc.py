import numpy as np
import math

def triArea(n1, n2, n3):
    a = ((n1['x'] - n2['x'])**2 + (n1['y'] - n2['y'])**2 + (n1['z'] - n1['z'])**2)**0.5
    b = ((n3['x'] - n2['x'])**2 + (n3['y'] - n2['y'])**2 + (n3['z'] - n1['z'])**2)**0.5
    c = ((n1['x'] - n3['x'])**2 + (n1['y'] - n3['y'])**2 + (n1['z'] - n3['z'])**2)**0.5
    h = (a + b + c) / 2
    area  = (h * (h - a) * (h - b) * (h - c))**0.5
    return area

def lineLength(n1, n2):
    res = ((n1['x'] - n2['x'])**2 + (n1['y'] - n2['y'])**2 + (n1['z'] - n2['z'])**2)**0.5
    return res

def func(a, b, c, d, x):
    res = a * x**3 + b * x**2 + c * x + d
    return res

def diffFunc(a, b, c, d, x):
    res = 3 * a * x**2 + 2 * b * x + c
    return res


def iterNode(nodeNum, cliques, nodelist):
    # 查找节点nodeNum所在的所有团，并过滤自己
    neighborCliques = []
    for clique in cliques:
        if nodeNum in clique:
            neighborCliques.append(list(filter(lambda x: x != nodeNum, clique.copy())))
    # 构建迭代方程的系数
    a = 0
    b = 0
    c = 0
    d = 0
    for neighborClique in neighborCliques:
        if len(neighborClique) == 2:
            # 3节点团
            xi2 = nodelist[neighborClique[0]]
            xi3 = nodelist[neighborClique[1]]
            xk = nodelist[nodeNum]
            area = triArea(xk, xi2, xi3)
            R = (xi2['value'] - xi3['value'])**2 / (area**3)
            a += 2 * R
            b -= 3 * R * (xi2['value'] + xi3['value'])
            c += R * (xi2['value']**2 + xi3['value']**2 + 4 * xi2['value'] * xi3['value'])
            d -= R * (xi2['value'] * xi3['value']**2 + xi2['value']**2 * xi3['value'])
        elif len(neighborClique) == 1:
            # 2节点团
            xj = nodelist[neighborClique[0]]
            xk = nodelist[nodeNum]
            length = lineLength(xj, xk)
            c += 2 / length**2
            d -= 2 * xj['value'] / length**2
    # 割线法迭代
    x0 = -20
    x1 = 20
    idx = 0
    while True:
        idx += 1
        x2 = x1 - func(a, b, c, d, x1) * (x1 - x0) / (func(a, b, c, d, x1) - func(a, b, c, d, x0))
        x0 = x1
        x1 = x2
        if math.fabs(x1 - x0) < 1e-3:
            nodelist[nodeNum]['value'] = x1
            break
        if idx > 100:
            break    
    # 牛顿迭代法
    # x0 = 0
    # while True:
    #     x1 = x0 - func(a, b, c, d, x0) / diffFunc(a, b, c, d, x0)
    #     if math.fabs(x1 - x0) < 1e-3:
    #         break
    #     x0 = x1
    # nodelist[nodeNum]['value'] = x0

# def tripleCliqueCalc(clique: list, nodelist, measureNodes: list):
#     if len(clique != 3):
#         print(clique)
#         print('不是3节点团')
#         return
#     tmp = {}
#     for idx, nodeNum in enumerate(clique):
#         # 如果不是计算节点则跳过
#         if nodeNum in measureNodes:
#             continue
#         i = 0
#         j = 0
#         for k in range(3):
#             if k != idx:
#                 i = k
#                 break
#         for k in range(3):
#             if k != idx and k !=i:
#                 j = k
#                 break
#         xi2 = nodelist[clique[i]]
#         xi3 = nodelist[clique[j]]
#         xk = nodelist[nodeNum]
#         area = triArea(xk, xi2, xi3)
#         R = (xi2['value'] - xi3['value'])**2 / (area**3)
#         a = 2 * R
#         b = -3 * R * (xi2['value'] + xi3['value'])
#         c = R * (xi2['value']**2 + xi3['value']**2 + 4 * xi2['value'] * xi3['value'])
#         d = -R * (xi2['value'] * xi3['value']**2 + xi2['value']**2 * xi3['value'])
#         x0 = 0
#         x1 = 10
#         while True:
#             x2 = x1 - func(a, b, c, d, x1) * (x1 - x0) / (func(a, b, c, d, x1) - func(a, b, c, d, x0))
#             x0 = x1
#             x1 = x2
#             if math.fabs(x1 - x0) < 1e-3:
#                 break
#         tmp[nodeNum] = x1
#     for idx, nodeNum in enumerate(clique):
#         if nodeNum in measureNodes:
#             continue
#         nodelist[nodeNum] = tmp[nodeNum]

# def doubleCliqueCalc(clique: list, nodelist, measureNodes: list):
#     if len(clique != 2):
#         print(clique)
#         print('不是2节点团')
#         return
#     tmp = {}
#     for idx, nodeNum in enumerate(clique):
#         # 如果不是计算节点则跳过
#         if nodeNum in measureNodes:
#             continue
#         j = 0
#         if idx == 0:
#             j = 1
#         else:
#             j = 0
#         xj = nodelist[clique[j]]
#         xk = nodelist[nodeNum]
#         len = lineLength(xj, xk)
#         a = 0
#         b = 0
#         c = 2 / (len**2)
#         d = -2 * xj['value'] / (len**2)
#         x0 = 0
#         x1 = 10
#         while True:
#             x2 = x1 - func(a, b, c, d, x1) * (x1 - x0) / (func(a, b, c, d, x1) - func(a, b, c, d, x0))
#             x0 = x1
#             x1 = x2
#             if math.fabs(x1 - x0) < 1e-3:
#                 break
#         nodelist[nodeNum] = x1