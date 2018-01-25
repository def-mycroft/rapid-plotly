"""Creates grouped barplot

For two groups only. Could create another script for more groups. 

Pass in_data. in_data is mean to be a dataframe in this manner:

                       bar1           bar2
x_category1            3.13          15.84
x_category2            6.67           6.08

Where in_data index is the x_categories and bar1/bar2 are like data.

In the above example, the 3.13 and 15.84 bars would be grouped 
together and the 6.67 and 6.08 bars would be grouped together. Bar1
would be on the left of each bar group.

There can only be two columns in in_data, but there can be unlimited 
rows, which means that there can be many categories, but only two 
categorized datasets (i.e. each barroup can only contain two bars).

"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def chart(in_data, filename, names1, names2,
        title='title', xlab='xlab', ylab='ylab'):

    trace1 = go.Bar(
            x=list(in_data.index),
            y=in_data[in_data.columns[0]],
            name=in_data.columns[0],
            text=['n = ' + str(x) for x in names1],
            marker=go.Marker(color='#3D3C28')
    )

    trace2 = go.Bar(
            x=list(in_data.index),
            y=in_data[in_data.columns[1]],
            name=in_data.columns[1],
            text=['n = ' + str(x) for x in names2],
            marker=go.Marker(color='#9B2D1E')
    )

    data = [trace1, trace2]

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
        )
    )

    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)
