"""Creates a multiple scatterplot
    17X20M JD - seems to be genearlly applicable. 
    Need review this and incorporate into chartslib project 
"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def chart(in_data, filename, 
        name='name', title='title', ylab='ylab', boxpoints=None):
    """Creates fancy boxplots with plotly.

    Uses same axes for both plots. 

    Boxpoints arg set to 'all' shows actual data points beside boxplot

    """
    # create box objects 
    data = [go.Box(

        y=in_data,
        name=name,
        boxpoints=boxpoints,
        boxmean=True,

        marker=dict(
            color='#3D3C28'
            ),
    )]


    # create layout
    layout = go.Layout(

            title=title,
            plot_bgcolor='rgb(229, 229, 229)',

            yaxis=dict(
                zerolinecolor='rgb(255,255,255)',
                gridcolor='rgb(255,255,255)',
                title=ylab
            ),

            annotations=[
                dict(
                    text='quantity in sample: %s' % len(in_data),
                    x=0,
                    y=int(0.75 * in_data.max()),
                    showarrow=False
                )],

            )

    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)
