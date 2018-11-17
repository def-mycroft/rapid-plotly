"""messy ad-hoc script for creating a stacked grouped barplot

may be able to mold this into something more generally applicable

"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def chart(in_data, offset, filename,
        title='title', xlab='xlab', ylab='ylab',
        annotation={'text':'', 'xloc':0, 'yloc':1}):
    """Creates a grouped-stacked barplot

    Only works for groups of three.

    As of now some of this is hard coded

    Input should be in this format, different table for each 
    member of the bargroup.

        x           stack                  y
        0-10K       content_development 19.0
        0-10K       creative_services   26.5
        0-10K       project_management  14.0
        10K-25K     content_development 19.0
        10K-25K     creative_services   25.5
        10K-25K     project_management  16.0
        25K-75K     content_development 16.0
        25K-75K     creative_services   34.5
        25K-75K     project_management   0.0
        75K-150K    content_development  0.0
        75K-150K    creative_services   37.5
        75K-150K    project_management   0.0
        150K+       content_development  0.0
        150K+       creative_services   42.0
        150K+       project_management   0.0

    """

    # set up data
    data = list()
    x_groups = in_data[0]['x'].unique().tolist()
    colors = {
            'content_development':'#9B2D1E',
            'project_management':'#3D3C28',
            'creative_services':'#0E5688'
            }

    def get_base(depts, sl):
        """Gets base for addition of block"""
        x = sl[sl['stack'].isin(depts)]
        return x.groupby('x', sort=False).sum()['y'].tolist()

    def append_trace(sl, department, name, base, position):
        """Appends a trace to data"""
        msg = '%s department expected' % department
        y_vals = sl[sl['stack'] == department]['y'].tolist()
        data.append(go.Bar(
                x=x_groups,
                y=y_vals,
                name=name,
                text=[str(x)+'<br>'+msg+'<br>'+name for x in y_vals],
                offset=position,
                width=offset,
                base=base,
                hoverinfo='text',
                marker=dict(
                    color=colors[department]
                    )
                ))

    # create plots for standard package
    sl = in_data[0]

    dept = 'content_development'
    append_trace(
            # data slice 
            sl,                 
            # department
            dept,
            # hover label
            'Standard Package',         
            # base arg
            0,                       
            # position arg
            -offset                     
            )

    dept = 'creative_services'
    append_trace(
            # data slice
            sl,                 
            # department
            dept,
            # hover text
            'Standard Package',       
            # base arg
            get_base(['content_development'], sl),
            # bar position
            -offset                  
            )

    dept = 'project_management'
    append_trace(
            # data slice
            sl,                 
            # department
            dept,
            # hover text
            'Standard Package',       
            # base arg
            get_base(['content_development', 'creative_services'], sl),
            # bar position
            -offset                  
            )

    # create plots for premium package
    sl = in_data[1]

    dept = 'content_development'
    append_trace(
            # data slice 
            sl,                 
            # department
            dept,
            # hover label
            'Premium Package',         
            # base arg
            0,                       
            # position arg
            0
            )

    dept = 'creative_services'
    append_trace(
            # data slice
            sl,                 
            # department
            dept,
            # hover text
            'Premium Package',       
            # base arg
            get_base(['content_development'], sl),
            # bar position
            0
            )

    dept = 'project_management'
    append_trace(
            # data slice
            sl,                 
            # department
            dept,
            # hover text
            'Premium Package',       
            # base arg
            get_base(['content_development', 'creative_services'], sl),
            # bar position
            0
            )

    # create plots for ultimate package
    sl = in_data[2]

    dept = 'content_development'
    append_trace(
            # data slice 
            sl,                 
            # department
            dept,
            # hover label
            'Ultimate Package',         
            # base arg
            0,                       
            # position arg
            offset
            )

    dept = 'creative_services'
    append_trace(
            # data slice
            sl,                 
            # department
            dept,
            # hover text
            'Ultimate Package',       
            # base arg
            get_base(['content_development'], sl),
            # bar position
            offset
            )

    dept = 'project_management'
    append_trace(
            # data slice
            sl,                 
            # department
            dept,
            # hover text
            'Ultimate Package',       
            # base arg
            get_base(['content_development', 'creative_services'], sl),
            # bar position
            offset                  
            )



    # create layout
    layout = go.Layout(

        title=title,
        barmode='stack',
        hovermode='closest',
        showlegend=False,

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
                text=annotation['text'],
                x=annotation['xloc'],
                y=annotation['yloc'],
                showarrow=False
            )
        ]

    )


    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)
