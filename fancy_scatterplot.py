"""Create a fancy scatterpot using plotly

Passing 'text' to hoverinfo arg forces the scatter point popups to
only show the 'names', else shows name and text.

TODO - want to be able to show inline in jupyter, create switch

TODO - see cvpl99020 project. have updated version of this which
allows for modification of layout by passing dict as arg. 

TODO - allow for custom annotation to be passed

"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
from scipy.stats import pearsonr as correl


def chart(x, y, names, filename,
          xlab='xlab', ylab='ylab', title='title',
          annotation_location=(0, 0), return_model=False, xtick_height=False,
          ytick_height=False, hoverinfo=None, suppress_model=False):
    """Given x, y creates a plot"""

    # create fancy scatterplot
    slope, intercept = np.polyfit(x, y, 1)
    xi = x
    line = slope * xi + intercept

    # define model
    def model(x, view_coefficients=False):
        """Simple model function"""
        # TODO have hacky way of viewing coefficients...
        # ...try to make this a property or something
        if view_coefficients:
            print('slope: %s' % slope)
            print('intercept: %s' % intercept)
        return slope * x + intercept

    # calculate r2 value
    r2 = correl(x, y)[0]**2

    # plot scatter points
    trace1 = go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=go.Marker(color='#3D3C28'),
        name=ylab,
        hoverinfo=hoverinfo,
        text=names,
    )

    # plot trendline
    trace2 = go.Scatter(
        x=xi,
        y=line,
        mode='lines',
        marker=go.Marker(color='#9B2D1E'),
        name='Fit'
    )

    # setup y ticks
    ydtick = ''
    if ytick_height == False:
        ydtick = max(y) / 20
    else:
        ydtick = ytick_height

    # setup x ticks
    xdtick = ''
    if xtick_height == False:
        xdtick = max(x) / 20
    else:
        xdtick = xtick_height

    # setup annotations
    annotations = [
        {
            'text': 'R^2: %s slope: %s' % (round(r2, 2), round(slope, 2)),
            'x': annotation_location[0],
            'y':annotation_location[1],
            'showarrow':False
        }
    ]

    # create data list
    data = [trace1, trace2]

    if suppress_model:
        annotations = []
        del data[-1]

    # create layout
    layout = go.Layout(

        title=title,
        plot_bgcolor='rgb(229, 229, 229)',

        xaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=xlab,
            dtick=xdtick
        ),

        yaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=ylab,
            dtick=ydtick
        ),

        annotations=annotations
    )

    # create figure 
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)

    # return model function
    if return_model:
        return model
