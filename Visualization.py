"""
Visualization module using Bokeh for displaying train, ideal, and test data.
This module provides a function to generate visualization that includes:
1. The training functions y1-y4
2. Best-matching ideal functions
3. Mapped test data points and their deviations
"""
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.models import HoverTool
import pandas as pd

def graph(traindataset: pd.DataFrame, mappeddata: pd.DataFrame, idealdataset: pd.DataFrame, selected: dict):
    """
    Plots training data, ideal functions, and mapped test data using Bokeh.
    This function generates two interactive plots:
    The first shows the original training functions and the selected ideal functions.
    The second shows test data points mapped to ideal functions.

    Output: Generates an HTML file 'plots.html' and opens it in a browser.
    """
    output_file("plots.html")

    p1 = figure(title="Training DataFrame and Ideal Functions", x_axis_label='x', y_axis_label='y', width=900, height=400)
    colors = ['blue', 'green', 'orange', 'purple']

    # training data
    for i in range(1, 5):
        p1.scatter(traindataset['x'], traindataset[f'y{i}'], color=colors[i - 1], size=5, legend_label=f"Train y{i}")

    # selected ideal functions
    for i, (train_col, ideal_col) in enumerate(selected.items()):
        p1.line(idealdataset['x'], idealdataset[ideal_col], line_width=2, color=colors[i], legend_label=f"Ideal {ideal_col}")

    p1.legend.click_policy = "hide"
    p1.add_tools(HoverTool(tooltips=[("x", "@x"), ("y", "@y")]))

    # test data mapping
    p2 = figure(title="Mapped Test DataFrame with Deviation", x_axis_label='x', y_axis_label='y', width=900, height=400)
    if not mappeddata.empty:
        mapper = {ideal: color for ideal, color in zip(selected.values(), colors)}
        for ideal_func, group in mappeddata.groupby('ideal_func'):
            p2.scatter(group['x'], group['y'],
                       color=mapper.get(ideal_func, 'gray'),
                       size=6,
                       legend_label=f"Mapped to {ideal_func}",
                       alpha=0.6)

    p2.legend.click_policy = "hide"
    p2.add_tools(HoverTool(tooltips=[("x", "@x"), ("y", "@y"), ("Δy", "@delta_y")]))

    show(column(p1, p2))
