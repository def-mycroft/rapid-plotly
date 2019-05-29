"""Convenience function for creating a Plotly scatterplot

Use `create_graph` to create an attractive, highly interactive Plotly
scatterplot, either in a Jupyter notebook or as an html file. 

"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd
from . import helpers
output_graph = helpers.output_graph


def create_trace(x, y, col, colors, names, hoverinfo):
    """Creates a scatter trace"""
    trace = go.Scatter(
        x=x[col],
        y=y[y.columns[0]],
        mode='markers',
        marker=go.scatter.Marker(color=colors[col]),
        hoverinfo=hoverinfo,
        text=names[col],
        name=col
    )

    return trace


def create_regression(x, y):
    """Creates a regression line for the graph

    The `r2` value is the "r-squared" or "explained variance" indicator.

    """
    # create regression line 
    slope, intercept = np.polyfit(x, y, 1)

    # calculate r2 value 
    r2 = pd.concat([x, y], axis=1).corr().iloc[0,1] ** 2

    regline = go.Scatter(
        x=x,
        y=intercept + x * slope,
        mode='lines',
        marker=go.scatter.Marker(color='red'),
        name='fit'
    )

    return regline, slope, intercept, r2


def create_graph(x_data, y_data, names='', colors='', regline=False,
                 title='title', xlab='xlab', ylab='ylab', hoverinfo=None,
                 annotations=[], filepath='', layout='', aux_traces=[],
                 figonly=False):
    """Creates a scatterplot

    `x_data` and `y_data` are expected to be dataframes or lists of 
    dataframes representing the x values and y values of the data. When
    passing a list of dataframes, the order of the list is used to 
    match up x and y values. 

    Parameters
    ----------
    x_data : DataFrame of x values.

    y_data : DataFrame of y values.

    names : DataFrame of hovertext values. Should mirror `x_data` or
    `y_data` in form. Column names must correlate to that of `in_data`.

    colors : dict or DataFrame of colors for traces. dict keys should
    mirror `in_data` columns. Can use hex colors or keyword colors, see
    Plotly specifications on colors for keyword options. 

    regline : passing True as `regline` adds a regression line on the
    graph. 

    title : title for top of graph. Use '<br>' tag for subtitle. Tags
    '<i>' and '<b>' can be used for italics and bold, respectively.

    xlab : label for x-axis. 

    ylab : label for y-ayis. 

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

    """
    # if x_data isn't a list, put it into a list  
    if not isinstance(x_data, list):
        x_data = [x_data]
        y_data = [y_data]

    # use default colors if none are passed
    # otherwise use passed dataframe
    if isinstance(colors, str):
        colors = x_data[0].copy()
        colors.loc[:, :] = '#232C65'

    # setup names and if nothing is passed
    if isinstance(names, str):
        names = x_data[0].copy()

    # create list of traces
    data = list()

    for i in range(len(x_data)):
        sl = x_data[i]
        for col in sl.columns:
            data.append(create_trace(x_data[i], y_data[i], col, colors,
                                     names, hoverinfo))

    # if regression, add regression trace to aux_traces
    # only works for the first scatter 
    if regline:
        reg, slope, intercept, r2 = create_regression(
                                      x_data[0][x_data[0].columns[0]],
                                      y_data[0][y_data[0].columns[0]],
                                  )

        aux_traces += [reg]

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

    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    output_graph(filepath=filepath, fig=fig, figonly=figonly)

    return fig
