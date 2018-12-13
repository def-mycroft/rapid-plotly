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


def create_errors(error, error_barwidth):
    """Creates dict of errors for barplot"""

    if isinstance(error, str):
        error_y = {}

    else:
        error_y = {
            'type': 'data',
            'array': error,
            'thickness': error_barwidth,
            'width': int((error_barwidth * 2.5) / 2),
            'visible': True
        }

    return error_y


def create_trace(in_data, colors, col, hoverinfo, names, errors,
                 error_barwidth):
    """Creates a barplot trace for a column in `in_data`"""
    if isinstance(errors, str):
        error_y = {}
    else:
        error_y = create_errors(errors[col], error_barwidth)

    trace = go.Bar(
        x=list(in_data.index),
        y=in_data[col],
        name=col,
        text=names[col],
        marker=go.bar.Marker(color=colors[col]),
        hoverinfo=hoverinfo,
        error_y=error_y
    )

    return trace


def create_graph(in_data, filepath='', names='', errors='', alt_y=False, title='title', xlab='xlab', ylab='ylab', y2lab='y2lab', colors='', error_barwidth=7, layout='', hoverinfo=None, annotations=[], aux_traces=[]):
    """Creates grouped barplot

    The `in_data` arg must be a dataframe in the form:

                           bar1           bar2
    x_category1            3.13          15.84
    x_category2            6.67           6.08

    Where `in_data.index` (x_category1, x_category2 above) are the x
    labels on the graph, and each column (bar1, bar2 in the above
    example) is a bargroup. Each cell represents the height of the bar.

    In the above example, the 3.13 and 15.84 bars would be grouped 
    together and the 6.67 and 6.08 bars would be grouped together. Bar1
    would be on the left of each bar group.

    Note that `in_data` can be passed with a single column to create
    a normal barplot (as opposed to a grouped barplot).

    There isn't an expected limit on the number of columns in `in_data`.

    If a filepath is passed, the graph will be written to an html file,
    otherwise the graph will be displayed in-line (when calling from a
    Jupyter notebook).

    A dataframe `names` can be passed; a dataframe with the same shape,
    index and columns as `in_data` where each cell represents the
    desired hover text for each bar. 

    A dataframe `errors` can be passed; a dataframe with the same shape,
    index and columns as `in_data` where each cell represents the
    below and above value for the error bar on each large bar, e.g.
    if the value is "5", the error bar will range from 5 units above
    the corresponding bar and 5 units below the corresponding bar. 

    The `error_barwidth` arg represents the width of the error bars in
    pixels.

    The `title`, `xlab` and `ylab` args are text arguments which 
    correspond to the main title, x label and y label of the graph. 

    The `colors` arg is a dict mapping columns of `in_data` to html
    colors for each bar. 

    Pass "'hoverinfo='text'" to strip the default values from the
    hovertext (and therefore only display the text passed in `names`).

    The annotations arg is expected to be a series of dicts in the form:

        {'text':'annotation text', 'x':10, 'y':15, 'showarrow'=False}

    By default, `plotly` defines the 'x' and 'y' values in terms of the 
    data on the graph. Annotations have a depth of features in `plotly`,
    refer to `plotly` documentation for annotation options.

    TODO - create method of editing axis parameters by keyword args.

    TODO - update docstring to explain alt trace. 

    Possible to add lines on alternate axes using `create_trace` and the
    `aux_traces` arg. The trace needs to be created outside of the script
    and passed as an arg.

    To create data on a second y-axis, pass `alt_y=True`, build a trace,
    pass the trace in a list as `aux_traces`.

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
        data.append(create_trace(in_data, colors, col, hoverinfo, names,
                                 errors, error_barwidth))

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
