"""Misc helper functions used across multiple types of graphs"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import plotly.io as pio
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


def to_image(fig, filepath, width=1000, height=450):
    """Writes plotly graph to image"""
    pio.write_image(fig, filepath, width=width, height=height)
    

def output_graph(fig, filepath, width=2000, height=900):
    """Given a Plotly fig, generates a graph

    If `filepath` is an empty string, display inline notebook, otherwise
    write a file to `filepath`. If `filepath` contains the file extension
    `.html`, a full interactive `.html` file is generated, if the file
    extension is `.png` a `.png` file is written.

    For the `.png` option, `width` and `height` are in pixels.

    """
    if filepath == '':
        init_notebook_mode(connected=True)
        iplot(fig)
    elif '.html' in filepath:
        plot(fig, filename=filepath, auto_open=False)
        
    elif '.png' in filepath:
        to_image(fig, filepath, width=width, height=height)


def default_colors(keys, colors=None):
    """Generates a repeating color pallette"""

    if colors == None:
        colors = ['#232C65', '#840032', '#E59500', '#00A6FB',
                  '#02040F', '#E4572E']
    colors = colors * (len(keys) + 1)

    return dict(zip(keys, colors[:len(keys)]))
