"""Creates a multiple boxplot 
"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def chart(in_data, names, filename, 
        name='name', title='title', ylab='ylab', boxpoints=None):
    """Creates fancy boxplots with plotly.

    Uses same axes for both plots. 

    Boxpoints arg set to 'all' shows actual data points beside boxplot

    """
    # create box objects 
    def create_plot(data_series, name):
        """Creates a boxplot"""
        box = go.Box(
            y=data_series,
            name=name,
            boxpoints=boxpoints,
            boxmean=True,
            marker=dict(
                color='#3D3C28'
                )
        )

        return box

    data = list()
    for name in names:
        series = in_data[name]
        total = '${:,.3f}'.format(series.sum() / 1000000)
        name = '%s<br>(n=%s, sum=%sM)' % (
                name, len(series), total
                )
        data.append(create_plot(series, name))

    # create layout
    layout = go.Layout(

            title=title,
            plot_bgcolor='rgb(229, 229, 229)',
            showlegend=False,

            yaxis=dict(
                zerolinecolor='rgb(255,255,255)',
                gridcolor='rgb(255,255,255)',
                title=ylab
            )
            )

    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)
