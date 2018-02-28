"""normal baryplot"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def create_trace(x_vals, y_vals, text, color, error=None):
    """Creates trace for barplot"""

    error_y = dict()

    if error == None:
        error_y = {
            'type':'data',
            'array':[0],
            'visible':False
        }

    else:
        error_y = {
            'type':'data',
            'array':[error],
            'visible':True
        }

    trace = go.Bar(
        x=x_vals,
        y=y_vals,
        text=text,
        marker=dict(
            color=color
        ),
        error_y=error_y
    )
    return trace


def chart(in_data, filename,
          title='title', xlab='xlab', ylab='ylab',
          colors=None):
    """Creates a normal barplot

    in_data is a dataframe containing columns 'x', 'y' and 'text' 
    where 'text' is the popup text on the bar hover text

    Optionally pass a dict mapping x values to colors.

    Example input:

        x                        y                    text
        Michael A Spencer       0.1742          Michael A Spencer
        Jordan T Cairns        -0.4665          Jordan T Cairns
        James Reilly            0.1361          James Reilly
        Rebecca J White         0.0389          Rebecca J White
        Alan N Montgomery       0.1749          Alan N Montgomery
        Daniel B Elmore         0.2429          Daniel B Elmore
        Solomon L Grover       -0.0191          Solomon L Grover
        Dan C Schultz Jr        0.5093          Dan C Schultz Jr
        Ahron M Jones          -0.0284          Ahron M Jones
        William H. Spicer III   0.1524          William H. Spicer III


    """

    if colors == None:
        colors = dict(zip(
            in_data['x'].unique(),
            ['#0E5688'] * len(in_data['x'])
        ))

    if 'error' not in in_data.columns:
        in_data['error'] = None

    data = list()
    for category in in_data['x'].unique():
        data.append(create_trace(
            in_data[in_data['x'] == category]['x'],
            in_data[in_data['x'] == category]['y'],
            in_data[in_data['x'] == category]['text'],
            colors[category],
            in_data[in_data['x'] == category]['error'].values[0]
        ))

    # create layout
    layout = go.Layout(

        title=title,
        plot_bgcolor='rgb(229, 229, 229)',
        showlegend=False,

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
