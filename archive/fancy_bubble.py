"""Use plotly to create a bubble plot 

Derived from this tutorial: https://plot.ly/python/bubble-charts/

"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
from scipy.stats import pearsonr as correl


def chart(x, y, sizes, filename, title='title', xlab='xlab', ylab='ylab',
          rangex='', rangey='', annotations=[]):
    """Create a bubble plot"""

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


def sample(out_path):
    """Use chart to generate a sample with annotations"""
    # revenues and subscribers data
    largest_bubble_size = 300
    subscribers = pd.Series([7, 10, 27])
    revenues = pd.Series([600, 1200, 2500])
    sizes = (revenues / revenues.max()) * largest_bubble_size

    # create annotations
    annotations = [
        dict(
            text='annotation text',
            x=20,
            y=2500,
            showarrow=False

        )

    ]

    # create chart
    chart(
        subscribers,
        revenues,
        sizes,
        out_path + 'test.html',
        title='Revenues vs Client Count',
        xlab='Revenue ($M)',
        ylab='Quantity of Clients',
        rangey=[0, 4000],
        rangex=[0, 35],
        annotations=annotations

    )
