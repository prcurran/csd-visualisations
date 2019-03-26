"""
Periodic table coloured by element frequency in the CSD

Code adapted from bokeh cookbook:
    - https://bokeh.pydata.org/en/latest/docs/gallery/periodic.html

Requires CSD count data
"""
from __future__ import print_function

import pandas as pd
from bokeh import palettes
from bokeh.io import output_file, show, export_png
from bokeh.models import LogColorMapper, LogTicker, ColorBar, TapTool, OpenURL
from bokeh.plotting import figure
from bokeh.sampledata.periodic_table import elements
from bokeh.transform import dodge, factor_cmap, linear_cmap, log_cmap


def _add_count_data(df):
    """
    append count data to the dataframe
    :param df: pandas dataframe
    :return: list
    """

    count = []
    for atm in df["symbol"]:
        try:
            count.append(count_data[atm])

        except KeyError:
            count.append(0)
    return count


cdf = pd.read_csv("count.csv")
output_file("periodic.html")
count_data = {cdf['element'][i]: cdf['csd'][i] for i in range(len(cdf))}

periods = ["I", "II", "III", "IV", "V", "VI", "VII", "","Lanthanides", "Actinides"]
groups = [str(x) for x in range(1, 19)]

df = pd.read_csv("Z:/github_packages/csd_visualisation/csd-visualisations/data/periodic_table.csv")
df["group"] = df["group"].astype(str)
df["count"] = _add_count_data(df)

TOOLTIPS = [
    ("Name", "@name"),
    ("Atomic number", "@{atomic number}"),
    ("Atomic mass", "@{atomic mass}"),
    ("Type", "@metal"),
    ("Count", '@count'),

]

p = figure(title="", plot_width=1000, plot_height=750,
           x_range=groups, y_range=list(reversed(periods)),
           tools="hover,tap", toolbar_location=None, tooltips=TOOLTIPS)

color_bar = ColorBar(color_mapper=LogColorMapper(palette=palettes.Plasma256, low=0, high=max(df['count'])),
                     orientation='horizontal', ticker=LogTicker(), padding=25, label_standoff=12,
                     border_line_color=None, title="Coloured by Element Frequency\n (low = purple, high = yellow)", location=(0,0),
                     major_label_text_color='black')

p.add_layout(obj=color_bar, place='above')

r = p.rect("group", "period", 0.95, 0.95, source=df, fill_alpha=0.6,
           color=log_cmap('count', palette=palettes.Plasma256, low=0, high=max(df['count']))
           )

text_props = {"source": df, "text_align": "left", "text_baseline": "middle"}

x = dodge("group", -0.4, range=p.x_range)

p.text(x=x, y="period", text="symbol", text_font_style="bold", **text_props)

p.text(x=x, y=dodge("period", 0.3, range=p.y_range), text="atomic number",
       text_font_size="10pt", **text_props)

# p.text(x=x, y=dodge("period", -0.35, range=p.y_range), text="name",
#        text_font_size="7pt", **text_props)

p.text(x=x, y=dodge("period", -0.2, range=p.y_range), text="atomic mass",
       text_font_size="7pt", **text_props)

p.text(x=["3", "3"], y=["VI", "VII"], text=["*", "**"], text_align="center", text_baseline="middle")

p.outline_line_color = None
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_standoff = 0
p.hover.renderers = [r]  # only hover element boxes

p.add_tools(TapTool())

url = "https://www.ccdc.cam.ac.uk/Community/educationalresources/PeriodicTable/@name"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)

show(p)
export_png(p, "periodic_table.png")

