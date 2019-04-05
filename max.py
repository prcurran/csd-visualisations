import pandas as pd
import numpy as np
import decimal

def frange(x, y, jump):
    """

    :param x:
    :param y:
    :param jump:
    :return:
    """
    while x < y:
        yield float(x)
        x += float(decimal.Decimal(jump))


year = 1985
df = pd.read_csv('Z:/github_packages/csd_visualisation/csd-visualisations/chemical_space/data/merge.csv')
df = df.loc[df['subset'] == 'drug']
df = df.loc[(df['year'] >= (year - 5)) & (df['year'] <= (year + 5))]

xedges = list(frange(-3, 3, '0.1'))
yedges = list(frange(-3, 3, '0.1'))

H, xedges, yedges = np.histogram2d(df.x, df.y, bins=(xedges, yedges), normed=True)
H = H.T  # Let each row list bins with common y range.
#
print np.unravel_index(np.argmax(H, axis=None), H.shape)

max = [35,7]
x = xedges[max[0]]
y = yedges[max[1]]
print x, y

df = df.loc[((df['y'] >= float(xedges[int(max[0])])) &
            (df['y'] <= float(xedges[int(max[0]+1)])) &
            (df['x'] >= float(yedges[int(max[1])])) &
            (df['x'] <= float(yedges[int(max[1]+1)])))
]

entries = list(df.refcode)
from ccdc.search import TextNumericSearch

data = []
# for e in entries:
#     query = TextNumericSearch()
#     query.add_all_identifiers(e)
#     hits = query.search()
#     data.append(hits[0].entry.publication.doi)
# from pprint import pprint
#
# print len(data)
# print len(set(data))
from ccdc.diagram import DiagramGenerator
from ccdc.io import EntryReader

diagram_generator = DiagramGenerator()
diagram_generator.settings.font_size = 12
diagram_generator.settings.line_width = 1.6
diagram_generator.settings.image_width = 500
diagram_generator.settings.image_height = 500

csd_reader = EntryReader('CSD')
mols = set([csd_reader.entry(m) for m in entries])

for i, e in enumerate(mols):
    img = diagram_generator.image(e)

    img.save("hit{}.png".format(i))
