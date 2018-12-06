"""Convenience function for creating a Plotly barplot

Use `create_graph` to create an attractive, highly interactive Plotly
barplot, either in a Jupyter notebook or as an html file. 

"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from copy import copy
import numpy as np
import pandas as pd
from . import helpers
output_graph = helpers.output_graph


def create_trace(in_data, colors, col, hoverinfo, names, yaxis=None):
    """Creates a barplot trace for a column in `in_data`"""
    trace = go.Scatter(
        x=list(in_data.index),
        y=in_data[col],
        mode='lines',
        name=col,
        text=names[col],
        marker=go.scatter.Marker(color=colors[col]),
        hoverinfo=hoverinfo,
        yaxis=yaxis
    )

    return trace


def create_graph(in_data, filepath='', names='', alt_y=False,
                 title='title', xlab='xlab', ylab='ylab', y2lab='y2lab', 
                 colors='', layout='', hoverinfo=None, annotations=[],
                 aux_traces=[]):
    """Creates a line plot 

    Possible to add lines on alternate axes using `create_trace` and the
    `aux_traces` arg.

    TODO - write docstring.

    """
    # use default colors if none are passed
    # otherwise use passed dataframe
    if isinstance(colors, str):
        colors = helpers.default_colors(in_data.columns)

    # setup names and errors if nothing is passed
    if isinstance(names, str):
        names = dict(zip(in_data.columns, in_data.columns))

    # create list of traces
    data = list()

    if alt_y:
        yaxis='y1' 

    for col in in_data.columns:
        data.append(create_trace(in_data, colors, col, hoverinfo, names, yaxis))

    # if more than one trace, add multiple traces 
    if len(aux_traces) > 0:
        for at in aux_traces:
            data.append(at)

    # create layout
    # if no layout is passed, use default layout from helpers
    if layout == '':
        layout = helpers.layout

    layout['title'] = title
    layout['xaxis']['title'] = xlab
    layout['yaxis']['title'] = ylab
    layout['annotations'] = annotations
    layout = go.Layout(layout)

    if alt_y:
        y = copy(layout['yaxis'])
        y['title'] = y2lab
        y['side'] = 'right'
        y['overlaying'] = 'y'
        layout['yaxis2'] = y

    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    output_graph(filepath=filepath, fig=fig)

    return fig
