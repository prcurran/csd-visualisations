import pandas as pd

from bokeh.plotting import figure
from bokeh.layouts import layout, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, Select
from bokeh.io import curdoc


def select_subset():
    """
    generates subset of dataframe from interactive controls
    """

    selected = df[
        (df.year >= min_year.value) &
        (df.year <= max_year.value)
    ]
    if (subset.value != "All"):
        selected = selected[selected.subset.str.contains(subset.value) == True]
    return selected


def update():
    """
    update the scatter plot
    """
    df = select_subset()
    source.data = dict(
        x=df["x"],
        y=df["y"],
        refcode=df["refcode"],
        year=df["year"],
        subset=df['subset'],
        colour=[colour_dic[a] for a in df['subset']]
    )

df = pd.read_csv('Z:/github_packages/csd_visualisation/csd-visualisations/chemical_space/data/merge.csv')

# Create Input controls
min_year = Slider(title="Min", start=1940, end=2019, value=2016, step=1)
max_year = Slider(title="Max", start=1940, end=2019, value=2019, step=1)
subset = Select(title="Subset", value="All", options=['drug', 'CSD', 'MOF', 'All'])

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], refcode=[], year=[], subset= [],colour=[]))

# Create hover information
TOOLTIPS = [("Refcode", "@refcode"),
            ("Year", "@year")
            ]
colour_dic = {'CSD': '#87CEFA',
              'drug': '#FA8072',
              'MOF': '#3CB371'}

# Initialise boundaries
left = min(set(df.x)) - 1
right = max(set(df.x)) + 1
top = max(set(df.y)) + 1
bottom = min(set(df.y)) - 1

# create and plot
p = figure(plot_height=600,
           plot_width=700,
           title="PCA analysis of the CSD",
           x_range=(left, right),
           y_range=(bottom, top),
           toolbar_location='below',
           tooltips=TOOLTIPS)

p.circle(x="x", y="y", source=source, size=4, fill_alpha=0.1, line_color='colour', color="colour")

controls = [min_year, max_year, subset]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = column(*controls, sizing_mode=sizing_mode)
l = layout([[inputs, p], ], sizing_mode=sizing_mode)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "ChemicalSpace"
