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


def create_graph(in_data, filepath='', names='', alt_y=False, title='title',
                 xlab='xlab', ylab='ylab', y2lab='y2lab', colors='', layout='',
                 hoverinfo=None, annotations=[], aux_traces=[], aux_first=False,
                 hovermode='closest', in_data_alt=None, colors_alt='',
                 names_alt=''):
    """Creates a line plot 

    Possible to add lines on alternate axes using `create_trace` and the
    `aux_traces` arg. The alt trace must be created and passed to this 
    function.

    TODO - write docstring.

    TODO - should be able to create alternate axes from the single
    function.

    """
    # setup colors
    # use default colors if none are passed
    # otherwise use passed dataframe
    if isinstance(colors, str):
        # default colors creates a dictionary where the coloumns
        # of in_datda are the keys, html color codes are the 
        # values
        colors = helpers.default_colors(in_data.columns)

    # if there are aux traces and no alt_colors, use reversed
    # default colors
    # colors are reversed in this case so that the alt traces have
    # different colors 
    if alt_y and isinstance(colors_alt, str):
        c = in_data_alt.columns.tolist()[::-1]
        alt_colors = helpers.default_colors(c)

    # setup names
    # setup names and errors if nothing is passed
    if isinstance(names, str):
        names = dict(zip(in_data.columns, in_data.columns))

    # same for alt names 
    if alt_y and isinstance(names_alt, str):
        names_alt = dict(zip(in_data_alt.columns, in_data_alt.columns))

    # create list of traces
    data = list()

    # if there is a secondary y axis, have to specify which axis is 
    # which, so specify yaxis as 'y1' if there is al alt y
    # by default `create_trace` requires `yaxis`, set to None if 
    # only a single axis
    yaxis = 'y1' if alt_y else None

    # create the main traces
    for col in in_data.columns:
        trace = create_trace(in_data, colors, col, hoverinfo, names, yaxis)
        data.append(trace)

    # create the alt traces
    if alt_y:
        alt_traces = []
        for col in in_data_alt.columns:
            trace = create_trace(in_data_alt, colors_alt, col, hoverinfo,
                                 names_alt, yaxis)
            alt_traces.append(trace)

        data += alt_traces

    # if more than one trace, add multiple traces 
    if len(aux_traces) > 0:
        if aux_first:
            data = aux_traces + data
        else:
            data = data + aux_traces

    # create layout
    # if no layout is passed, use default layout from helpers
    if layout == '':
        layout = helpers.layout

    layout['title'] = title
    layout['xaxis']['title'] = xlab
    layout['yaxis']['title'] = ylab
    layout['annotations'] = annotations

    if hovermode == 'closest':
        layout['hovermode'] = 'x'
    else:
        layout['hovermode'] = hovermode

    layout = go.Layout(layout)

    # if alt_y, duplicate `yaxis`, modify and use as a `yaxis2`.
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
