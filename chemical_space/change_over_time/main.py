# import seaborn as sns
import pandas as pd
# # import matplotlib.pyplot as plt
# #
# # df = pd.read_csv('merge.csv')
# # df = df.loc[df['subset'] == 'drug']
# # ax = sns.kdeplot(df["x"], df["y"], shade=True)
# # plt.show()


import numpy as np

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bokeh.util.hex import hexbin
from bokeh.models.widgets import Slider, Select
from bokeh.plotting import figure
from bokeh.layouts import layout, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, Select
from bokeh.io import curdoc

def select_subset():
    """
    generates subset of dataframe from interactive controls
    """

    selected = df[df.year <= (year.value + 5) & df.year >= (year.value - 5)]
    return selected


def update():
    """
    update the scatter plot
    """
    df = select_subset()
    bins = hexbin(df.x, df.y, 0.08)
    source.data = dict(
        x=bins["q"],
        y=bins["r"],
        counts=bins["counts"]

    )



year = Slider(title="Min", start=1940, end=2020, value=1950, step=10)
source = ColumnDataSource(data=dict(x=[], y=[], counts=[]))

df = pd.read_csv('Z:/github_packages/csd_visualisation/csd-visualisations/chemical_space/data/merge.csv')
df = df.loc[df['subset'] == 'drug']
bins = hexbin(df.x, df.y, 0.08)
#print bins

# Initialise boundaries
left = min(set(df.x)) - 1
right = max(set(df.x)) + 1
top = max(set(df.y)) + 1
bottom = min(set(df.y)) - 1
TOOLTIPS= [("x", "@x"),
           ("y", "@y")]

p = figure(title="CSD drug subset",
           tools="wheel_zoom,pan,reset",
           match_aspect=True,
           x_range=(left, right),
           y_range=(bottom, top),
           background_fill_color='#440154',
           tooltips=TOOLTIPS)
p.grid.visible = False

p.hex_tile(q="x", r="y", size=0.08, line_color=None, source=source,
           fill_color=linear_cmap('counts', 'Viridis256', 0, max(bins.counts)))

controls = [year]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = column(*controls, sizing_mode=sizing_mode)
l = layout([[inputs, p], ], sizing_mode=sizing_mode)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "DrugSpace"