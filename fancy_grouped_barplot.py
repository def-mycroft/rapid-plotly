import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def chart(in_data, filename, colors, errors='', title='title', xlab='xlab', ylab='ylab', names='', error_barwidth=7, hoverinfo=None, custom_annotations=[]):
    """Creates grouped barplot

    Pass in_data. in_data is mean to be a dataframe in this manner:

                           bar1           bar2
    x_category1            3.13          15.84
    x_category2            6.67           6.08

    Where in_data index is the x_categories and bar1/bar2 are like data.

    Pass "'hoverinfo='text'" to strip the default values from the
    hovertext.

    In the above example, the 3.13 and 15.84 bars would be grouped 
    together and the 6.67 and 6.08 bars would be grouped together. Bar1
    would be on the left of each bar group.

    There isn't an expected limit on the width of `in_data`.

    The `names` arg is expected to be a dict where the keys are the 
    columns of `in_data` and the values are names for each category
    bar in each of the columns, i.e. a list of length equal to
    len(in_data.index). Each error value is the "+/-" value for the bar,
    e.g. if the cell value is "15", then the error bar will be 15 units
    above and 15 units below the top of the bar.

    The `colors` arg is a dict mapping columns of `in_data` to html
    colors on the graph

    Error bars can be added by passing a dataframe with the same
    index and columns as `in_data`, where each cell value is the error
    for the corresponding bar in `in_data`. 

    TODO - have a `DepreciationWarning` related to `Marker`. 

    """
    def create_errors(error):
        """Creates error dict"""

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

    def create_trace(col, hoverinfo, names, errors):
        """Creats a trace"""

        if isinstance(errors, str):
            error_y = {}
        else:
            error_y = create_errors(errors[col])

        trace = go.Bar(
                x=list(in_data.index),
                y=in_data[col],
                name=col,
                text=names[col],
                marker=go.Marker(color=colors[col]),
                hoverinfo=hoverinfo,
                error_y=error_y
        )

        return trace

    # setup names and errors if nothing is passed
    if names == '':
        names = dict(zip(in_data.columns, in_data.columns))

    # create list of traces 
    data = list()
    for col in in_data.columns:
        data.append(create_trace(col, hoverinfo, names, errors))

    # create layout
    layout = go.Layout(

        title=title,
        plot_bgcolor='rgb(229, 229, 229)',

        xaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=xlab,
        ),

        yaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=ylab,
        ),

        annotations=custom_annotations,
        hovermode='closest'
    )

    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename, auto_open=False)

    return fig
