"""Function for generic plotly plots"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def chart(data, filename,
        xlab='xlab', ylab='ylab', title='title',
        annotation={'text':'', 'xloc':0, 'yloc':1},
        layout=None):
    """Highly configurable plotly plot generator

    Should be able to pass plotly data objects as "data" and output
    chart as normal.

    """

    # if no layout passed, use standard layout, 
    # else layout must be passed as arg
    if layout == None:
        layout = go.Layout(

            title=title,

            plot_bgcolor='rgb(229, 229, 229)',

            xaxis=dict(
                zerolinecolor='rgb(255,255,255)',
                gridcolor='rgb(255,255,255)',
                title=xlab
            ),

            yaxis=dict(
                zerolinecolor='rgb(255,255,255)',
                gridcolor='rgb(255,255,255)',
                title=ylab
            ),

            annotations=[
                dict(
                    text=annotation['text'],
                    x=annotation['xloc'],
                    y=annotation['yloc'],
                    showarrow=False
                )
            ]

        )

    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)
