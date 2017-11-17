"""Script to create simple matplotlib scatterplot"""

from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import pearsonr
import pandas as pd

def simple_chart(col, df, return_model=False, descriptive=True):
    """Create simple scatterplot with slope and r2 data

    Plots `col` against population

    """
    xlab = 'population'
    ylab = col
    fig, ax = plt.subplots(figsize=(10, 10))

    # create x and y data from dataframe
    m1 = df.client_category == 'City'
    m2 = (df.population < 150000) & (df.population.notnull())
    sl = df[m1 & m2]
    x = sl.population
    y = sl[col]

    # create trendline and plot
    fit = np.polyfit(x, y, 1)

    def model(x):
        return fit[0] * x + fit[1]

    ax.plot(x, model(x), color='red')

    # labels and title
    plt.xlabel(xlab)
    plt.ylabel(ylab)

    # annotate text
    r2 = round(pearsonr(x, y)[0]**2, 2)
    ax.text(
        0, 
        y.max() * 0.85,
        'r2: %s slope: %s intercept: %s' % (r2, round(fit[0], 2), round(fit[1], 2)))

    # plot scatterplot
    plt.scatter(x, y)

    # plot descriptive stats
    if descriptive:
        print(x.describe())
        print('')
        print(y.describe())

    plt.grid()
    plt.show()
    plt.close()

    if return_model:
        return model
