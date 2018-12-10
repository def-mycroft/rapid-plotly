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


def create_graph(x_data, y_data, filepath='', names='', colors='', regline=False,
                 title='title', xlab='xlab', ylab='ylab', layout='',
                 hoverinfo=None, annotations=[], aux_traces=[]):
    """Creates a scatterplot

    `x_data` and `y_data` are expected to be dataframes or lists of 
    dataframes representing the x values and y values of the data. When
    passing a list of dataframes, the order of the list is used to 
    match up x and y values. 

    If a filepath is passed, the graph will be written to an html file,
    otherwise the graph will be displayed in-line (when calling from a
    Jupyter notebook).

    A dataframe `names` can be passed where each column of the dataframe
    corresponds to the column name of `x_data` or to the names in each
    dataframe in the list `x_data`.

    A dataframe `colors` can be passed in a similar fashion to `names`, 
    where each cell is a hex color code. 

    The `title`, `xlab` and `ylab` args are text arguments which 
    correspond to the main title, x label and y label of the graph. 

    The annotations arg is expected to be a series of dicts in the form:

        {'text':'annotation text', 'x':10, 'y':15, 'showarrow'=False}

    By default, `plotly` defines the 'x' and 'y' values in terms of the 
    data on the graph. Annotations have a depth of features in `plotly`,
    refer to `plotly` documentation for annotation options.

    Axis labels are inferred from columns in `x_data` and `y_data`.

    TODO - need to just pass a series as x and y, or maybe a single 
    dataframe. Right now it is set up for an awkward way of plotting
    multiple series, which shoudl be superseded by aux_traces. (Will 
    have to modify the regline `if` statement among other things after 
    fixing this).

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
    output_graph(filepath=filepath, fig=fig)

    return fig
