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


def create_graph(in_data, names='', colors='', errors='', error_barwidth=4, 
                 title='title', xlab='xlab', ylab='ylab', y2lab='y2lab',
                 hoverinfo=None, annotations=[], filepath='', aux_traces=[],
                 layout='', alt_y=False, aux_first=False, figonly=False):
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

    Error bars can be easily created by passing a DataFrame similar
    to `in_data` where each cell represents the "+/-" value for the
    error bar, e.g. if the value is "1.5", the error bar will range 
    "1.5" units (in terms of the y-axis) above and "1.5" units below
    the bar.

    The `aux_traces` arg can be used to create an overlaying trace, such
    as a line graph overlaying the bars. To plot `aux_traces` on a 
    secondary axis, the `yaxis` parameter of the trace must be set to
    'y2' and the `alt_y` arg must be passed to this function as `True`.

    Parameters
    ----------
    in_data : DataFrame of traces. Data in columns will be used as
    traces and index will be used as x-axis.

    names : DataFrame of hovertext values. Should mirror `in_data` in 
    form.

    colors : dict of colors for traces. dict keys should mirror
    `in_data` columns. Can use hex colors or keyword colors, see Plotly
    specifications on colors for keyword options.

    errors : a DataFrame of error values for each bar. Should mirror 
    `in_data` in form. Each cell in `errors` will be the "+/-" value 
    for the error bars. 

    error_barwidth : the width, in pixels, of the error bar. 

    title : title for top of graph. Use '<br>' tag for subtitle. Tags
    '<i>' and '<b>' can be used for italics and bold, respectively.

    xlab : label for x-axis. 

    ylab : label for y-ayis. 

    y2lab : label for aly y axis.

    hoverinfo : either None or 'text'. Passed to the trace in
    `create_trace`. By default, Plotly displays the value upon hover,
    passing 'text' here will show only the value configured in the
    `names` DataFrame.

    annotations : a list of dicts for annotations. For example:

        ```
        [{'text':'More cylinders correlates to better<br> fuel mileage',
        'x':1.5, 'y':24.5, 'showarrow':False}]
        ```

    The 'x' and 'y' keys are coordinates in terms of the graph axes, and
    the 'text' key is the annotation text.

    filepath : optional, if included will write image to file. Can be
    written as a .html file or a .png file.

    aux_traces : list of traces to be added to the graph data. Allows
    for customization of additional traces beyond what default
    functionality provides. 

    aux_first : bool, if True then aux traces will be added first.

    layout : allows for a customized layout. Default layout is in the
    helpers module, can be accessed:

        ```
        from rapid_plotly import helpers
        layout = helpers.layout
        ```

    Here is the default layout: 

        ```
        {'hovermode': 'closest', 'plot_bgcolor': 'rgb(229, 229, 229)',
         'title': 'title', 'xaxis': {'gridcolor': 'rgb(255,255,255)',
          'tickangle': 30, 'title': 'xlab',
          'zerolinecolor': 'rgb(255,255,255)'},
          'yaxis': {'gridcolor': 'rgb(255,255,255)', 'title': 'ylab',
          'zerolinecolor': 'rgb(255,255,255)'}}
        ```

    alt_y : bool, used to place aux_traces on alternate axis. 

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

    # create and append traces 
    for col in in_data.columns:
        data.append(create_trace(in_data, colors, col, hoverinfo, names,
                                 errors, error_barwidth))

    # if more than one trace, add multiple traces...
    # ... and change order of traces depending on aux_first
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
    output_graph(filepath=filepath, fig=fig, figonly=figonly)

    return fig
