"""Misc helper functions used across multiple types of graphs"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import plotly.io as pio
import pandas as pd
from PIL import Image

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


def image_rotate(fp1, fp2):
    """Transposes an image at a path, writes to new path"""
    im = Image.open(fp1)
    im = im.transpose(Image.ROTATE_90)
    im.save(fp2)


def generate_annotations(in_data, textangle=0, vertical_offset=0.05,
                         text_formatter=None, textfont={}):
    """Generates annotations above each bar in a barplot

    Still under development 

    `in_data` should be the same input as passed to
    `barplot.create_graph`. The text is inferred from `in_data`. 

    Inferring the locations using the below logic: 
    
    One unit in terms of x on grouped barplot is:

    $$
    BarsPerUnit = NumberBarsPerGroup + 1
    $$

    To move location by one bar unit: 

    $$
    OneBarWidth = \frac{1}{BarsPerUnit}
    $$

    ...and one half a barwidth is of course

    $$
    OneHalfBarWidth = \frac{1}{2 BarsPerUnit}
    $$

    To get distance of one half barwidth:

    $$
    OneHalfBarWidth = \frac{1}{2(NumberBarsperGroup + 1)}
    $$    


    TODO - continue testing this and add to barplot.py, also 
    to the examples dict.

    """
    vertical_offset = in_data.max().max() * vertical_offset
    bargroups_count = len(in_data.index)
    bars_perbargroup = len(in_data.columns)
    onehalfbarwidth = 1 / (2*(bars_perbargroup + 1))
    barwidth = onehalfbarwidth * 2 
    
    if not text_formatter:
        text_formatter = lambda x: x

    # creat mapping of bar numbers to x-axis locations
    mapping = dict(zip(
        range(1,(bars_perbargroup+1)),
        np.arange(-bars_perbargroup,(bars_perbargroup+1),2)
    ))
    # function to generate xlocaiotn 
    f = lambda x: onehalfbarwidth * mapping[x] + onehalfbarwidth

    annt = list()

    for bargroup, index in enumerate(in_data.index.tolist()):
        for bar, col in enumerate(in_data.columns.tolist()):
            a = {
                'x':bargroup+f(bar+1),
                'y':in_data.loc[index, col]+vertical_offset,
                'text':text_formatter(in_data.loc[index, col]),
                'showarrow':False,
                'xref':'x',
                'align':'center',
                'textangle':textangle,
                'font':textfont,
            }
            annt.append(a)
            
    return annt


def create_band(sl, color='rgba(26,150,65,0.25)', upper_col='upper',
                lower_col='lower'):
    """Creates traces that form a colored background band

    By default assumes that `sl` contains a column `upper` and a column
    `lower`, otherwise args `upper_col` and `lower_col` can be used to 
    specify which traces in `sl` are the upper part of the band and 
    which are the lower part of the band. 

    An `rbga` argument is passed as `color`.

    The result will probably be best if these are the first traces in
    the list of traces. 

    TODO: lower line is visible on band, need to set the opacity or 
    something to make the lower line invisible. 

    """
    band_lower = go.Scatter(
        x=sl.index,
        y=sl[lower_col],
        name='lower',
        mode='lines',
        fill=None,
        marker=go.scatter.Marker(color=color),
        showlegend=False,
        hoverinfo='none',
        opacity=1,
    )

    band_upper = go.Scatter(
        x=sl.index,
        y=sl[upper_col],
        name='upper',
        fill='tonexty',
        mode='none',
        fillcolor=color,
        marker=go.scatter.Marker(color=color),
        showlegend=False,
        hoverinfo='none',
    )

    return [band_lower, band_upper]


def to_image(fig, filepath, width=680, height=520, scale=None,
             orient='horizontal'):
    """Writes plotly graph to image

    If `orient` is 'vertical', then width and height are swapped.

    TODO - experiment with the scale param, see [here][1], might make 
    for better graphs sometimes

    [1]: https://plot.ly/python/static-image-export/
    """
    if orient == 'vertical':
        # swap width and height param
        c = (width, height)
        height, width = c

    pio.write_image(fig, filepath, width=width, height=height, scale=scale)
    

def output_graph(fig, filepath, width=680, height=520, figonly=False,
                 scale=None, orient='horizontal'):
    """Given a Plotly fig, generates a graph

    If `filepath` is an empty string, display inline notebook, otherwise
    write a file to `filepath`. If `filepath` contains the file extension
    `.html`, a full interactive `.html` file is generated, if the file
    extension is `.png` a `.png` file is written.

    For the `.png` option, `width` and `height` are in pixels.

    """
    if filepath == '':
        init_notebook_mode(connected=True)
        if not figonly:
            iplot(fig)

    elif '.html' in filepath:
        plot(fig, filename=filepath, auto_open=False)
        
    elif '.png' in filepath:
        to_image(fig, filepath, width=width, height=height, scale=scale, 
                 orient=orient)


def default_colors(keys, colors=None, reverse=False):
    """Generates a repeating color pallette

    A list of colors can be passed to the `colors` arg.

    The `reverse` arg, if `True`, reverses `colors` before building the 
    dictionary.

    """

    if colors == None:
        colors = ['#232C65', '#840032', '#E59500', '#00A6FB',
                  '#02040F', '#E4572E']

    if reverse:
        colors = colors[::-1]

    colors = colors * (len(keys) + 1)

    return dict(zip(keys, colors[:len(keys)]))


def simple_line_trace(in_data, color='#E4572E', yaxis=None,
                      name='linetrace'):
    """Creates a simple linetrace"""
    trace = go.Scatter(
        x=list(in_data.index),
        y=in_data[in_data.columns[0]],
        mode='lines',
        marker=go.scatter.Marker(color=color),
        yaxis=yaxis,
        name=name,
    )

    return trace
