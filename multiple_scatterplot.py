"""Creates a multiple scatterplot

    Need review this and incorporate into chartslib project 

"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
from scipy.stats import pearsonr as correl


def chart(
        x, y1, y2, names, filename,
        title='graph title',
        xlab='x label', 
        ylab='y label',
        y1_lab='y1 label',
        y2_lab='y2 label',  
        xtick_height=False,
        ytick_height=False,
        y1_msgloc=(0,0), 
        y2_msgloc=(0,0)):
    """Given x, y1, y2 creates a plot"""

    # plot first set of scatter points
    trace1 = go.Scatter(
        x=x,
        y=y1,
        mode='markers',
        marker=go.Marker(color='#3D3C28'),
        name='Y1: ' + y1_lab,
        text=names
    )

    # plot second set of scatter points
    trace2 = go.Scatter(
        x=x,
        y=y2,
        mode='markers',
        marker=go.Marker(color='green'),
        name='Y2: ' + y2_lab,
        text=names
    )

    # create trendline for y1
    slope, intercept = np.polyfit(x, y1, 1)
    line = slope * x + intercept

    # calculate r2 values 
    r2y1 = correl(x, y1)[0]**2

    # plot for x and y1
    trace3 = go.Scatter(
        x=x,
        y=line,
        mode='lines',
        marker=go.Marker(color='black'),
        name='Y1 Fit'
    )

    # create trendline for y2
    slope, intercept = np.polyfit(x, y2, 1)
    line = slope * x + intercept

    # calculate r2 values 
    r2y2 = correl(x, y2)[0]**2

    # plot for x and y2
    trace4 = go.Scatter(
        x=x,
        y=line,
        mode='lines',
        marker=go.Marker(color='blue'),
        name='Y2 Fit'
    )

    # setup y ticks 
    ydtick = ''
    if ytick_height == False:
        ydtick = max(y1) / 20
    else:
        ydtick = ytick_height

    # setup x ticks 
    xdtick = ''
    if xtick_height == False:
        xdtick = max(x) / 20
    else:
        xdtick = xtick_height

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

        annotations=[

            dict(
                text='Y1 r^2: %s' % round(r2y1, 2),
                x=y1_msgloc[0],
                y=y1_msgloc[1],
                showarrow=False
            ),

            dict(
                text='Y2 r^2: %s' % round(r2y2, 2),
                x=y2_msgloc[0],
                y=y2_msgloc[1],
                showarrow=False
            )

        ]
    )

    # create figure
    data = [trace1, trace2, trace3, trace4]
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)
