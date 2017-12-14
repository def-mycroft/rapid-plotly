"""Creates a multiple scatterplot
    17X20M JD - seems to be genearlly applicable. 
    Need review this and incorporate into chartslib project 
"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def chart(in_data, filename):

    data = [go.Histogram(x=in_data)]

    # create figure
    fig = go.Figure(data=data)

    # output
    plot(fig, filename=filename)
