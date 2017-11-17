import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
from scipy.stats import pearsonr as correl

def create_chart(
        x, y, names, 
        out_path=False, anxloc=0, anyloc=0, xy_label=False, title=False, 
        display_para=False):
    """Given x, y creates a plot"""
    # filename for output file
    filename =''
    if not out_path:
        filename = 'test'
        filename += '.html'
    else:
        filename = out_path + '.html'

    # define labels
    x_label = ''
    y_label = ''

    if not xy_label:
        x_label = 'x label'
        y_label = 'y label'
    else:
        x_label = xy_label[0]
        y_label = xy_label[1]

    if not title:
        title = 'graph title'

    # create fancy scatterplot
    slope, intercept = np.polyfit(x, y, 1)
    xi = x
    line = slope * xi + intercept
    if display_para:
        print('slope:', slope)
        print('intercept:', intercept)

    # calculate r2 value
    r2 = correl(x, y)[0]**2

    # plot scatter points
    trace1 = go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=go.Marker(color='#3D3C28'),
        name=y_label,
        text=names
    )

    # plot trendline
    trace2 = go.Scatter(
        x=xi,
        y=line,
        mode='lines',
        marker=go.Marker(color='#9B2D1E'),
        name='Fit'
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
            title=y_label
        ),

        annotations=[
            dict(
                text='R^2: %s' % round(r2, 2),
                x=0,
                y=0,
                showarrow=False
            )
        ]
    )

    # create figure
    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)

    # output 
    plot(fig, filename=filename)
