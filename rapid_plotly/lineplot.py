"""Convenience function for creating a Plotly barplot

Use `create_graph` to create an attractive, highly interactive Plotly
barplot, either in a Jupyter notebook or as an html file. 

"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd
import helpers
output_graph = helpers.output_graph


def create_trace(in_data, colors, col, hoverinfo, names):
    """Creates a barplot trace for a column in `in_data`"""
    trace = go.Scatter(
        x=list(in_data.index),
        y=in_data[col],
        mode='lines',
        name=col,
        text=names[col],
        marker=go.scatter.Marker(color=colors[col]),
        hoverinfo=hoverinfo
    )

    return trace


def create_graph(in_data, filepath='', names='', errors='',
                 title='title', xlab='xlab', ylab='ylab', colors='',
                 layout='', hoverinfo=None, annotations=[]):
    """Creates grouped barplot

    The `in_data` arg must be a dataframe in the form:

                           bar1           bar2
    x_category1            3.13          15.84
    x_category2            6.67           6.08

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

    for col in in_data.columns:
        data.append(create_trace(in_data, colors, col, hoverinfo, names))

    # create layout
    # if no layout is passed, use default layout from helpers
    if layout == '':
        layout = helpers.layout

    layout['title'] = title
    layout['xaxis']['title'] = xlab
    layout['yaxis']['title'] = ylab
    layout['annotations'] = annotations
    layout = go.Layout(layout)

    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    output_graph(filepath, fig)

    return fig
