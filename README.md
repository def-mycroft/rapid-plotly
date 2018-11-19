# Functionality to rapidly create Plotly graphs 

The [Plotly][1] library facilitates the creation of beautiful and interactive
graphs. However, it takes at least several hundred lines of code to create a
presentable Plotly graph. Writing hundreds of lines of code every time a graph
is needed isn't feasible for professionals who work with data and it isn't fun
for people working on side projects.

Use `rapid_plotly` to quickly create beautiful and interactive Plotly graphs,
or use as a starting point to create your own toolbox of Plotly graph templates.

Current features:

* Functions designed to rapidly prototype Plotly graphs.
* Option to view graphs in Jupyter or to write graph to an html file.
* Barplots, optionally grouped, with error bars and custom hover text.
* Scatterplots, with custom hover text and option to overlay multiple datasets.

## Basic Usage

The below shows the basic functionality of `rapid_plotly`. The [Jupyter notebook included in the examples folder of this repo][2] contains more comprehensive examples. 

Given a pandas dataframe `in_data` in this form: 

|             | mpg  |
|-------------|------|
| 4 Cylinders | 26.6 |
| 6 Cylinders | 19.7 |
| 8 Cylinders | 15.1 |

The below code can be used to view a Plotly barplot in a Jupyter notebook:

```py
from rapid_plotly import barplot

args = {'in_data':in_data}

# view plot inline 
fig = barplot.create_graph(**args)

```

This creates a barplot where each bar is labeled by the index of `in_data` and the height of each bar is determined by `in_data['mpg']`.

After previewing the graph in Jupyter, the graph can be written to an html file by passing `fig` to `rapid_plotly.barplot.output_graph`:


```py
# write graph to html file 
fp = 'barplot-example.html'
barplot.output_graph(fp, fig)
```

## Installation

`rapid_plotly` was built on Plotly 3.4.1 and Python 3.7.1. Plotly can be
installed [via pip][3] or [via conda][4]. The pandas library can be installed
by following [instructions here][5].

First, clone this repo:

```sh
git clone https://github.com/def-mycroft/rapid-plotly.git && cd rapid-plotly
```

And then install using `pip`:

```sh
pip install .
```

## How to Contribute 

The goal of `rapid_plotly` is to create functionality to rapidly and effectively
create beautiful and highly interactive Plotly graphs. Any type of contribution
that helps this end is very much welcome!

Right now, `rapid_plotly` only has scatterplot and grouped/non-grouped
functionality, additional common graph types could be added (e.g. line graph,
treemap, choropleth or histogram).

New functionality could be built into the current graph functions as well, for
example the barplot script could be upgraded to create the option of having
multiple y axes. 

Enhancements which upgrade the usability and efficiency of `rapid_plotly` are 
also welcomed. For example, as of this writing the `rapid_plotly.scatterplot` 
module requires passing multiple dataframes with x and y coordinate points.
Someone else may think of a more efficient and simple way to plot x and y 
coordinates from multiple series of data.

If you're familiar with the Plotly libary (or want to learn), you could create
enhancements and submit a pull request. Or, you could submit an issue with a
enhancement suggestion. 


[1]: https://plot.ly/python/
[2]: https://nbviewer.jupyter.org/github/def-mycroft/rapid-plotly/blob/master/examples/Create%20Example%20Graphs.ipynb
[3]: https://plot.ly/python/getting-started/#installation
[4]: https://anaconda.org/plotly/plotly
[5]: https://pandas.pydata.org/
