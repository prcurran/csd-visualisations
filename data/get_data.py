"""

Throw-away script

"""

import os
import pandas as pd
from ccdc.io import EntryReader


class Organiser(object):

    def __init__(self):

        d = "CSD_Drug_Subset_updated.gcd"
        m = "MOF_subset.gcd"

        self.drugs = self.get_refcodes(d)
        self.mofs = self.get_refcodes(m)

        self.subset = []
        self.refcode = []
        self.year = []
        self.smiles = []

        self.data = [self.get_information(entry) for entry in EntryReader('CSD')]

    def get_information(self, entry):
        """
        collect data from the CSD
        :param entry:
        :param subset:
        :param refcode:
        :param year:
        :param smiles:
        :return:
        """
        ref = entry.identifier
        # 1
        self.refcode.append(ref)
        s = 'CSD'

        if ref in self.drugs:
            s = 'drug'

            if ref in self.mofs:
                s = 'both'

        elif ref in self.mofs:
            s = 'MOF'

        else:
            s = 'CSD'

        # 2
        self.subset.append(s)

        # 3
        self.year.append(entry.publication.year)

        # 4
        self.smiles.append(entry.molecule.smiles)

    @staticmethod
    def get_refcodes(fname):
        """
        get refcodes from file
        :return:
        """
        base = "C:/Program Files (x86)/CCDC/CSD_2019/CSD_540/subsets"
        return set(open(os.path.join(base, fname)).read().split("\n"))

    def to_df(self):
        return pd.DataFrame({'refcode': self.refcode,
                             'year': self.year,
                             'smiles': self.smiles,
                             'subset': self.subset
                             })


o = Organiser()
df = o.to_df()
df.to_csv("data.csv")

