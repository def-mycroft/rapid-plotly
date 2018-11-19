# Functionality to rapidly create Plotly graphs 

Use `rapid_plotly` to quickly create beautiful and interactive Plotly graphs,
or use as templates to create your own Plotly convenience functions. 

Current features:

* Barplots, optionally grouped, with error bars and custom hover text.
* Scatterplots, with custom hover text and option to overlay multiple datasets.
* Option to view graphs in Jupyter or to write graph to an html file.

## Basic Usage

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>mpg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4 Cylinders</th>
      <td>26.663636</td>
    </tr>
    <tr>
      <th>6 Cylinders</th>
      <td>19.742857</td>
    </tr>
    <tr>
      <th>8 Cylinders</th>
      <td>15.100000</td>
    </tr>
  </tbody>
</table>
</div>

## Installation

```sh
pip install gspread
```
