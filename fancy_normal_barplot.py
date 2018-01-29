"""normal baryplot"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def chart(in_data, filename,
        title='title', xlab='xlab', ylab='ylab'):
    """Creates a normal barplot

    in_data is a dataframe containing columns 'x', 'y' and 'text' 
    where 'text' is the popup text on the bar hover text

    """

    trace1 = go.Bar(
        x=in_data['x'],
        y=in_data['y'],
        text=in_data['text'],
        marker=dict(
            color='#0E5688'
        )
    )

    data = [trace1]

    # create layout
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
        )
    )


    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)
