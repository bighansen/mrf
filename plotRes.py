import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
plt.figure(figsize=(6.4, 3.5))
plt.subplots_adjust(bottom=0.16, left=0.12, top=0.95, right=0.88)
df = pd.read_csv('data/data_boxplot_vertical.csv', header=0, sep=',')
mrfdict = defaultdict(list)
stodict = defaultdict(list)
for idx, row in df.iterrows():
    if (int(row['num'])%5 != 0):
        continue
    mrfdict[row['num']].append(row['MRF'])
    stodict[row['num']].append(row['stochastic'])
mrf = pd.DataFrame(mrfdict)
mrf.boxplot(showfliers=False, showmeans=False, meanline=False, capprops={'color': '#0070c0'})
sto = pd.DataFrame(stodict)
stocbp = sto.boxplot(sym='', showfliers=False, showmeans=False, meanline=False, capprops={'color': '#bf7600'}, return_type='dict')
[item.set_color('#bf7600') for item in stocbp['boxes']]
[item.set_color('#bf7600') for item in stocbp['whiskers']]
t = np.arange(1, 12, 0.2)
l1, = plt.plot(t, -6e-5*(t*5)**2+0.0116*(t*5)+0.5107, label='MRF', color='#0070C0')
l2, = plt.plot(t, 0.0127*t*5+0.2334, label='stochastic', linestyle='--', color='#bf7600')
# plt.xlim(range(0,13), ['0','5','10', '15','20','25','30','35','40','45','50','55','60'])
plt.xlim((0, 12))
plt.ylim((0,1))
plt.xticks(range(1, 13), fontsize=12)
plt.yticks(np.arange(0, 1.2, 0.2), fontsize=12)
plt.xlabel('count of measured nodes', fontsize=12)
plt.ylabel('PCC value (mm)', fontsize=12)
plt.grid(False)

ax1 = plt.twinx()
ttest = pd.read_csv('data/data_t_test.csv', header=0, sep=',')
l3, = ax1.plot(ttest['num']/5, ttest['value'], color='gray', linestyle='-.', label='P(Sig.)')
ax1.set_ylim((0,0.6))
ax1.set_ylabel('P(Sig.)', fontsize=12)
# plt.legend(handles=[l3], labels=['P(Sig.)'], loc='lower center', fontsize=11)
plt.legend(handles=[l1, l2, l3], labels=['MRF PCC', 'stochastic PCC', 'P(Sig.)'], loc='lower center', bbox_to_anchor=(0.6,0.1), fontsize=11)

plt.savefig('res/fig.png')
plt.show()

