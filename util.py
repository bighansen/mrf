import pandas as pd
import numpy as np
import random
import math

from globalVariables import nodeMap


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