import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def chart(in_data, filename,
        title='title', xlab='xlab', ylab='ylab'):

    trace1 = go.Bar(
            x=list(in_data.index),
            y=in_data[in_data.columns[0]],
            name=in_data.columns[0],
            marker=go.Marker(color='#3D3C28')
    )

    trace2 = go.Bar(
            x=list(in_data.index),
            y=in_data[in_data.columns[1]],
            name=in_data.columns[1],
            marker=go.Marker(color='#9B2D1E')
    )

    data = [trace1, trace2]

    # create layout
    layout = go.Layout(

        title=title,
        plot_bgcolor='rgb(229, 229, 229)',

        xaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=xlab,
        ),

        yaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=ylab,
        )
    )

    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)
