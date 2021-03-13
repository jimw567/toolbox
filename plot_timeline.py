import plotly.figure_factory as ff
from datetime import datetime
import numpy as np


def int2dt(x):
    return datetime.fromtimestamp(31536000+x*24*3600).strftime("%Y-%d-%m")


df = [dict(Task="T111111111111111", Start=int2dt(0), Finish=int2dt(1), Resource='Func1'),
      dict(Task="T111111111111111", Start=int2dt(3), Finish=int2dt(4), Resource='Func2'),
      dict(Task="T222222222222222", Start=int2dt(5), Finish=int2dt(6), Resource='Func1'),
      dict(Task="T222222222222222", Start=int2dt(7), Finish=int2dt(8), Resource='Func2'),
]

colors = {'Func1': 'rgb(220, 0, 0)',
          'Func2': 'rgb(0, 255, 100)'}
fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                      group_tasks=True)

num_tick_labels = np.linspace(start=0, stop=10, num=11, dtype=int)
date_ticks = [int2dt(x) for x in num_tick_labels]
fig.layout.xaxis.update({'tickvals': date_ticks, 'ticktext': num_tick_labels})
fig.show()
