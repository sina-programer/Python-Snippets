import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

names = [
    'v2.2.4', 'v3.0.3', 'v3.0.2', 'v3.0.1', 'v3.0.0', 'v2.2.3',
    'v2.2.2', 'v2.2.1', 'v2.2.0', 'v2.1.2', 'v2.1.1', 'v2.1.0',
    'v2.0.2', 'v2.0.1', 'v2.0.0', 'v1.5.3', 'v1.5.2', 'v1.5.1',
    'v1.5.0', 'v1.4.3', 'v1.4.2', 'v1.4.1', 'v1.4.0'
]

dates = [
    '2019-02-26', '2019-02-26', '2018-11-10', '2018-11-10',
    '2018-09-18', '2018-08-10', '2018-03-17', '2018-03-16',
    '2018-03-06', '2018-01-18', '2017-12-10', '2017-10-07',
    '2017-05-10', '2017-05-02', '2017-01-17', '2016-09-09',
    '2016-07-03', '2016-01-10', '2015-10-29', '2015-02-16',
    '2014-10-26', '2014-10-18', '2014-08-26'
]
levels = [-5 ,5, -3 ,3 ,-1 ,1 ,-5 ,5 ,-3 ,3 ,-1 ,1 ,-5 ,5 ,-3 ,3 ,-1 ,1 ,-5 ,5 ,-3 ,3 ,-1]
dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]

fig, ax = plt.subplots(figsize=(8.8, 4))
ax.set(title="Matplotlib release dates")
ax.vlines(dates, 0, levels, color="red")
ax.plot(dates, np.zeros_like(dates), "-o",color="k", markerfacecolor="w")

for d, l, r in zip(dates, levels, names):
           ax.annotate(r, xy=(d, l),
           xytext=(0,0), textcoords="offset points",
           horizontalalignment="right",
           verticalalignment="bottom" if l > 0 else "top")

ax.get_yaxis().set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

plt.show()
