"""Choropleth map

Must pass in_data as a dataframe like this:

    states	categories	text
    AK	          3	         AK
    AL	          2	         AL
    AR	          0	         AR
    AZ	          3	         AZ
    CA	          3	         CA
    CO	          3	         CO
    CT	          1	         CT
    DE	          1	         DE
    FL	          2	         FL
    GA	          2	         GA
    HI	          3	         HI
    IA	          3	         IA
    ID	          3	         ID
    IL	          0	         IL
    IN	          2	         IN


TODO don't know how to actually control the colors. thought it
was about the z arg in go.Choropleth

"""
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd


def chart(in_data, color_map, filename,
        title='title'):

    data = list()

    def create_map(states, text, color):
        x = go.Choropleth(
            z=[1] * len(states),
            autocolorscale=False,
            colorscale=[[0, '#FFFFFF'], [1, color]],
            hoverinfo='text',
            locationmode='USA-states',
            locations=states,
            showscale=False,
            text=text,
            zauto=False,
            zmax=1,
            zmin=0,
        )

        return x

    # create data object
    for category in in_data.categories.unique():
        sl = in_data[in_data.categories == category].copy()
        states = sl.states
        text = sl.text
        color = color_map[category]
        trace = create_map(states, text, color)
        data.append(trace)

    # create layout
    layout = go.Layout(
        autosize=True,

        geo=dict(
            #countrycolor='rgb(255, 255, 255)',
            countrywidth=1,
            lakecolor='rgb(255, 255, 255)',
            landcolor='rgb(255, 255, 255)',

            lonaxis=dict(
                gridwidth=1.5999999999999999,
                range=[-180, -50],
                showgrid=False
            ),

            projection=dict(
                type='albers usa'
            ),

            scope='usa',
            showland=True,
            showrivers=False,
            showsubunits=True,
            subunitcolor='rgb(255, 255, 255)',
            subunitwidth=0.5
        ),

        hovermode='closest',
        showlegend=True,
        title=title
    )

    # create figure
    fig = go.Figure(data=data, layout=layout)

    # output
    plot(fig, filename=filename)
