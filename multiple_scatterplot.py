import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
from scipy.stats import pearsonr as correl


def create_chart(
        x, y1, y2, names,
        out_path=False, filename='test.html', anxloc=0, anyloc=0,
        xy1_label=('x label', 'y1 label'), title='graph title',
        y2_label='y2 label', yax_title='y axis title', 
        y1msgloc=(0,0), y2msgloc=(0,0)):
    """Given x, y1, y2 creates a plot"""
    # filename for output file
    filename += '.html'
    if not out_path:
        filename = out_path + filename
    else:
        filename = out_path + filename

    # setup labels
    x_label = xy1_label[0]
    y1_label = xy1_label[1]

    # plot first set of scatter points
    trace1 = go.Scatter(
        x=x,
        y=y1,
        mode='markers',
        marker=go.Marker(color='#3D3C28'),
        name=y1_label,
        text=names
    )

    # plot second set of scatter points
    trace2 = go.Scatter(
        x=x,
        y=y2,
        mode='markers',
        marker=go.Marker(color='green'),
        name=y2_label,
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

    # create layout
    layout = go.Layout(

        title=title,
        plot_bgcolor='rgb(229, 229, 229)',

        xaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=x_label
        ),

        yaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=yax_title
        ),

        annotations=[

            dict(
                text='y1 R^2: %s' % round(r2y1, 2),
                x=y1msgloc[0],
                y=y1msgloc[1],
                showarrow=False
            ),

            dict(
                text='y2 R^2: %s' % round(r2y2, 2),
                x=y2msgloc[0],
                y=y2msgloc[1],
                showarrow=False
            )

        ]
    )

    # create figure
    data = [trace1, trace2, trace3, trace4]
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)
