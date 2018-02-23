"""Function for generic plotly plots"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def chart(x_values, filename,
          xlab='xlab', ylab='ylab', title='title', tickvals=None,
          ticktext=None, text=None,
          bins={'start': '', 'end': '', 'size': ''},
          annotation={'text': '', 'xloc': 0, 'yloc': 1}):
    """Generates a histogram

    Note that the brackets are [lower,upper), python style.

    """
    data = list()

    # if x axis passed, create names else no names
    names = None
    hoverinfo = None
    if bins['start'] != '':
        names = list()
        hoverinfo = 'text'
        for x in range(int(bins['end'] / bins['size'])):
            names.append(
                'count between ' + \
                str(tickvals[x]) + '-' + str(tickvals[x + 1])
                )

    data.append(go.Histogram(
        x=x_values,
        nbinsx=bins,
        xbins=bins,
        hoverinfo='y+text',
        text=names
    ))

    # create layout
    layout = go.Layout(

        title=title,

        plot_bgcolor='rgb(229, 229, 229)',

        xaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=xlab,
            showticklabels=True,
            tickvals=tickvals,
            ticktext=ticktext
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
