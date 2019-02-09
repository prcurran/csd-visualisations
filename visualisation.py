# https://bokeh.pydata.org/en/latest/docs/gallery/periodic.html

from __future__ import print_function

import pandas as pd
from bokeh import palettes
from bokeh.io import output_file, show
from bokeh.models import LogColorMapper, LogTicker, ColorBar, TapTool, OpenURL
from bokeh.plotting import figure
from bokeh.sampledata.periodic_table import elements
from bokeh.transform import dodge, factor_cmap, linear_cmap, log_cmap


def _add_count_data(df):
    count = []
    for atm in df["symbol"]:
        try:
            count.append(count_data[atm])

        except KeyError:
            count.append(0)
    return count


cdf = pd.read_csv("data.csv")
output_file("periodic.html")
count_data = {cdf['element'][i]: cdf['frequency'][i] for i in range(len(cdf))}

periods = ["I", "II", "III", "IV", "V", "VI", "VII"]
groups = [str(x) for x in range(1, 19)]

df = elements.copy()
print(df["atomic mass"])
df["atomic mass"] = df["atomic mass"].round(decimals=int(2))

    #.astype(str)
df["group"] = df["group"].astype(str)
df["period"] = [periods[x - 1] for x in df.period]
df["count"] = _add_count_data(df)

print(df["count"])

print(sum(df["count"]))

df = df[df.group != "-"]
df = df[df.symbol != "Lr"]
df = df[df.symbol != "Lu"]

TOOLTIPS = [
    ("Name", "@name"),
    ("Atomic number", "@{atomic number}"),
    ("Atomic mass", "@{atomic mass}"),
    ("Type", "@metal"),
    ("Count", '@count'),

]

p = figure(title="Elements in the CSD", plot_width=1000, plot_height=550,
           x_range=groups, y_range=list(reversed(periods)),
           tools="hover,tap", toolbar_location=None, tooltips=TOOLTIPS)

color_bar = ColorBar(color_mapper=LogColorMapper(palette=palettes.Plasma256, low=0, high=max(df['count'])),
                     orientation='horizontal', ticker=LogTicker(), padding=50, label_standoff=1000,
                     border_line_color=None, title="Colour Map")

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

p.text(x=["3", "3"], y=["VI", "VII"], text=["LA", "AC"], text_align="center", text_baseline="middle")

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
