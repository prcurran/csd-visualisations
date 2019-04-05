from matplotlib.image import NonUniformImage
import matplotlib.pyplot as plt
import numpy as np
import decimal
import pandas as pd
from pprint import pprint

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


def diff(year):
    df = pd.read_csv('Z:/github_packages/csd_visualisation/csd-visualisations/chemical_space/data/merge.csv')
    df = df.loc[df['subset'] == 'drug']
    df = df.loc[(df['year'] >= (year-5)) & (df['year'] <= (year+5))]

    xedges = list(frange(-3, 3, '0.2'))
    yedges = list(frange(-3, 3, '0.2'))

    H, xedges, yedges = np.histogram2d(df.x, df.y, bins=(xedges, yedges), normed=True)
    H = H.T  # Let each row list bins with common y range.




    fig = plt.figure(figsize=(10, 10))

    ax = fig.add_subplot(111, title='Year {} +- 5'.format(year))
    plt.imshow(H, interpolation='nearest', origin='low', extent=[float(xedges[0]),
                                                                 float(xedges[-1]),
                                                                 float(yedges[0]),
                                                                 float(yedges[-1])
                                                                 ]
               )

    plt.savefig("{}-02.png".format(year))


for i in range(1955, 2025, 10):
    diff(i)
