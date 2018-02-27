"""Creates a multiple boxplot"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def chart(in_data, category_col, data_col, filename,
          name='name', title='title', ylab='ylab', boxpoints=None):
    """Creates fancy boxplots with plotly.

    Boxpoints arg set to 'all' shows actual data points beside boxplot

    Example data input:

        sales_rep          percent_from_model
        Solomon L Grover      -0.0828
        Justin C Blecha       -0.1051
        Rebecca J White        0.7145
        Jordan T Cairns       -0.7353
        Justin R Hammon       -0.7065
        Justin C Blecha       -0.4243
        John L Pugh           -0.2618
        Daniel B Elmore       -0.2304
        James Reilly           0.4012
        Jacob T Bertram       -0.9181

    To plot this data, pass category_col='sales_rep' and
    data_col='percent_from_model'

    """
    # create box objects
    def create_plot(data_series, name):
        """Creates a boxplot"""
        box = go.Box(
            y=data_series,
            name=name,
            boxpoints=boxpoints,
            boxmean=True,
            marker=dict(
                color='#3D3C28'
            )
        )

        return box

    data = list()
    for category in in_data[category_col].unique():
        series = in_data[in_data[category_col] == category][data_col]
        name = '%s (n=%s)' % (
            category, len(series)
        )
        data.append(create_plot(series, name))

    # create layout
    layout = go.Layout(

        title=title,
        plot_bgcolor='rgb(229, 229, 229)',
        showlegend=False,

        yaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=ylab
        )
    )

    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)
