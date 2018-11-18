

layout = {
    'hovermode': 'closest',
    'plot_bgcolor': 'rgb(229, 229, 229)',
    'title': 'title',
    'xaxis': {'gridcolor': 'rgb(255,255,255)', 'tickangle': 30, 'title': 'xlab',
              'zerolinecolor': 'rgb(255,255,255)'},
    'yaxis': {'gridcolor': 'rgb(255,255,255)', 'title': 'ylab',
              'zerolinecolor': 'rgb(255,255,255)'}
}

def create_errors(error, error_barwidth):
    """Creates error dict"""

    if isinstance(error, str):
        error_y = {}

    else:
        error_y = {
            'type': 'data',
            'array': error,
            'thickness': error_barwidth,
            'width': int((error_barwidth * 2.5) / 2),
            'visible': True
        }

    return error_y
 

def default_colors(keys, colors=None):
    """Generates a repeating color pallette"""
    
    if colors == None:
        colors = ['#232C65', '#840032', '#E59500', '#00A6FB',
                  '#02040F', '#E4572E']
    colors = colors * (len(keys)+1)
    
    return dict(zip(keys, colors[:len(keys)]))
