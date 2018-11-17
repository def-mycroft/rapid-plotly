def generate_layout(title='', xlab='', ylab='',
                   annotation={'text':'', 'xloc':0, 'yloc':1}):
    """Generates a layout
    
    Saving this here for use elsewhere. Written for cvpl99690 

    Could use this as a function to pass into my plotly_generic
    script and/or could copy/paste this into a notebook.

    """
    xticks = list(range(0,196+7,7))

    x_axis = go.XAxis(
        title=xlab,
        range=[0,xticks[-1]], # inclusive 
        zerolinecolor='rgb(255,255,255)',                                   
        gridcolor='rgb(255,255,255)',
        showticklabels=True,
        tickvals=list(xticks), # where are the markers
        ticktext=[str(x) + ' (%s weeks)' % (int(x/7)) for x in xticks] # labels for markers
    )


    layout = go.Layout(

        title=title,
        barmode='stack',
        showlegend=False,

        plot_bgcolor='rgb(229, 229, 229)',
        xaxis=x_axis,
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
    return layout
