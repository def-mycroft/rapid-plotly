"""Create a fancy scatterpot using plotly

TODO - want to be able to show inline in jupyter, create switch

"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
from scipy.stats import pearsonr as correl


def chart(x, y, names, filename,
          xlab='xlab', ylab='ylab', title='title',
          annotation_location=(0, 0), return_model=False):
    """Given x, y creates a plot"""

    # create fancy scatterplot
    slope, intercept = np.polyfit(x, y, 1)
    xi = x
    line = slope * xi + intercept

    # define model 
    def model(x):
        """Simple model function"""
        return slope*x + intercept

    # calculate r2 value
    r2 = correl(x, y)[0]**2

    # plot scatter points
    trace1 = go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=go.Marker(color='#3D3C28'),
        name=ylab,
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
            title=xlab
        ),

        yaxis=dict(
            zerolinecolor='rgb(255,255,255)',
            gridcolor='rgb(255,255,255)',
            title=ylab
        ),

        annotations=[
            dict(
                text='R^2: %s slope: %s' % (round(r2, 2), round(slope, 2)),
                x=annotation_location[0],
                y=annotation_location[1],
                showarrow=False
            )
        ]
    )

    # create figure
    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)

    # return model function
    if return_model:
        return model
