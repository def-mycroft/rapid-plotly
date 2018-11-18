"""Misc helper functions used across multiple types of graphs"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd

# default layout
layout = {
    'hovermode': 'closest',
    'plot_bgcolor': 'rgb(229, 229, 229)',
    'title': 'title',
    'xaxis': {'gridcolor': 'rgb(255,255,255)', 'tickangle': 30, 'title': 'xlab',
              'zerolinecolor': 'rgb(255,255,255)'},
    'yaxis': {'gridcolor': 'rgb(255,255,255)', 'title': 'ylab',
              'zerolinecolor': 'rgb(255,255,255)'}
}


def output_graph(filepath, fig):
    """Given a Plotly fig, generates a graph

    If `filepath` is an empty string, display inline notebook, otherwise
    write an html file to `filepath`.

    """
    if filepath == '':
        init_notebook_mode(connected=True)
        iplot(fig)
    else:
        plot(fig, filename=filepath, auto_open=False)


def default_colors(keys, colors=None):
    """Generates a repeating color pallette"""

    if colors == None:
        colors = ['#232C65', '#840032', '#E59500', '#00A6FB',
                  '#02040F', '#E4572E']
    colors = colors * (len(keys) + 1)

    return dict(zip(keys, colors[:len(keys)]))
