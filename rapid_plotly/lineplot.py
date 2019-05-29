"""Convenience function for creating a Plotly lineplot

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
    """Creates a lineplot trace for a column in `in_data`"""
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


def create_graph(in_data, names='', colors='', title='title', xlab='xlab',
                 ylab='ylab', y2lab='y2lab', alt_trace_cols=[],
                 hovermode='compare', hoverinfo=None, annotations=[],
                 filepath='', aux_traces=[], aux_first=False, layout='',
                 alt_y=False, in_data_alt=None, colors_alt='', names_alt='',
                 figonly=False):
    """Creates a line plot 

    Where `in_data` is a DataFrame of lines with the index as the
    x-axis.

    Columns of `in_data` passed in `alt_trace_cols` will be plotted on
    a secondary (right) y-axis.

    Parameters
    ----------
    in_data : DataFrame of traces. Data in columns will be used as
    traces and index will be used as x-axis.

    names : DataFrame of hovertext values. Should mirror `in_data` in 
    form.

    colors : dict of colors for traces. dict keys should mirror
    `in_data` columns. Can use hex colors or keyword colors, see Plotly
    specifications on colors for keyword options.

    title : title for top of graph. Use '<br>' tag for subtitle. Tags
    '<i>' and '<b>' can be used for italics and bold, respectively.

    xlab : label for x-axis. 

    ylab : label for y-ayis. 

    y2lab : label for aly y axis.

    alt_trace_cols : a subset of columns in in_data. Columns in this 
    list will be plotted on a right-side y axis. Args colors and names
    will be used for the alt axis.

    hovermode : hovermode passed to layout. Arg 'closest' will only
    show hovertext for data point nearest to cursor. Passing 'compare'
    other arg will pass 'x' to `layout['hovermode']`, which sets
    "Compare data on hover" as default. Otherwise, the arg will be
    passed to `layout['hovermode']`, see [Plotly documentation][1]
    for more info.

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

    alt_y : bool. If True, expect to have in_data_alt, colors_alt, 
    names_alt. Alternative to passing alt_trace_cols, typically won't
    be used.

    in_data_alt : similar to in_data, but will be plotted on alt axis.

    colors_alt : similar to colors, but applied to in_data_alt if 
    in_data_alt passed specifically. 

    names_alt : similar to names, but applied to in_data_alt if
    in_data_alt passed specifically. 

    [1]:https://plot.ly/python/reference/#layout-hovermode
    """
    # setup alt traces 
    if alt_trace_cols != []:
        alt_y = True
        in_data_alt = in_data[alt_trace_cols].copy()
        in_data = in_data[[
            x for x in in_data.columns if x not in in_data_alt.columns
        ]].copy()

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
        colors_alt = helpers.default_colors(c, reverse=True)

    # setup names
    # setup names and errors if nothing is passed
    if isinstance(names, str):
        names = dict(zip(in_data.columns, in_data.columns))

    # same for alt names 
    if alt_y and isinstance(names_alt, str) and not (len(alt_trace_cols) > 0):
        names_alt = dict(zip(in_data_alt.columns, in_data_alt.columns))

    # if alt cols passed, duplicate names 
    elif alt_y and len(alt_trace_cols) > 0:
        names_alt = names.copy()

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
        yaxis = 'y2'
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
        layout['hovermode'] = hovermode
    elif hovermode == 'compare':
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
    output_graph(filepath=filepath, fig=fig, figonly=figonly)

    return fig
