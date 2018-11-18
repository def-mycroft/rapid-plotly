"""Convenience function for creating a Plotly scatterplot

Use `create_graph` to create an attractive, highly interactive Plotly
scatterplot, either in a Jupyter notebook or as an html file. 

"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd
import helpers
output_graph = helpers.output_graph


def create_trace(in_data, col, colors, names, hoverinfo):
    """Creates a scatter trace for a column in `in_data`"""
    trace = go.Scatter(
        x=in_data.index,
        y=in_data[col],
        mode='markers',
        marker=go.scatter.Marker(color=colors[col]),
        hoverinfo=hoverinfo,
        text=names[col],
        name=col
    )

    return trace


def create_graph(in_data, filepath='', names='', errors='',
                 title='title', xlab='xlab', ylab='ylab', colors='', layout='',
                 hoverinfo=None, annotations=[]):
    """Creates a scatterplot

    Infers axis labels from `in_data`

    TODO - Write docs 

    TODO - split x and y values in `in_data`, can't use index for x values
    """
    # use default colors if none are passed
    # otherwise use passed dataframe
    if isinstance(colors, str):
        colors = in_data.copy()
        colors.loc[:, :] = '#232C65'

    # setup names and errors if nothing is passed
    if isinstance(names, str):
        names = in_data.copy()

    if xlab == 'xlab':
        xlab = in_data.index.name

    if ylab == 'ylab':
        ylab = in_data.columns[0]

    # create list of traces
    data = list()

    for col in in_data.columns:
        data.append(create_trace(in_data, col, colors, names, hoverinfo))

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
