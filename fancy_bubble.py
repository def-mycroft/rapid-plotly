"""Use plotly to create a bubble plot 


"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
from scipy.stats import pearsonr as correl


def chart(x, y, sizes, filename, title='title', xlab='xlab', ylab='ylab',
        rangex='', rangey='', annotations=[]):

    trace0 = go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(
            size=sizes,
            color='#9B2D1E'
        )
    )

    layout = go.Layout(

        title=title,
        plot_bgcolor='rgb(229, 229, 229)',

        xaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=xlab,
            range=rangex
        ),

        yaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=ylab,
            range=rangey
        ),
        annotations=annotations
    )

    # create figure
    data = [trace0]
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)
