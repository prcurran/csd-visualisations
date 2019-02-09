"""
TO DO: use substructure searching the HitProcessor to speed up searching

"""
from __future__ import print_function

import os
import pandas as pd
from ccdc.io import EntryReader, csd_directory
from tqdm import tqdm

from elements import ELEMENTS
from pprint import pprint


atoms = set([e.symbol for e in ELEMENTS])


class ElementCounter(object):
    """class to handle element counting"""
    def __init__(self, count, fname=None):
        self.count = count
        if fname:
            self.fname = fname
            self.count.to_csv(self.fname)

    @staticmethod
    def from_file(fname):
        """
        creates a dataframe from csv
        :param str fname: path to output file
        :return:
        """
        df = pd.read_csv(fname, index_col=0)
        return ElementCounter(count=df)

    @staticmethod
    def from_database(db, fname):
        """
        creates a dataframe from csd data
        :return:
        """
        #home = csd_directory()
        home = "C:/Program Files (x86)/CCDC/CSD_2019/CSD_540/subsets/"
        options = {'CSD': 'CSD',
                   'Drug': os.path.join(home, 'CSD_Drug_Subset_updated.gcd'),
                   'MOF': os.path.join(home, 'MOF_subset.gcd')}

        count = {e.symbol: 0 for e in ELEMENTS}
        for entry in tqdm(EntryReader(options[db])):
            for atm in entry.molecule.atoms:
                if atm.atomic_symbol in count:
                    count[atm.atomic_symbol] += 1

        df = pd.DataFrame({'element': [key for key in count.keys()],
                           'frequency': [value for value in count.values()]})

        return ElementCounter(count=df, fname=fname)


def main():
    #csd_elements = ElementCounter.from_database(db='CSD', fname="csd_elements.csv")
    csd_elements = ElementCounter.from_file("csd_elements.csv")
    d = atoms - set(csd_elements.count["element"])
    df = pd.DataFrame({"elements": d,
                       "count": [0] * len(d)
                       })

    csd_elements.count.append(df)

    drug_elements = ElementCounter.from_file("drug_elements.csv")
    mof_elements = ElementCounter.from_file("mof_elements.csv")

    # drug_elements = ElementCounter.from_database(db='Drug', fname="drug_elements.csv")
    # mof_elements = ElementCounter.from_database(db='MOF', fname="mof_elements.csv")

    data = pd.merge(pd.merge(csd_elements.count, drug_elements.count, on='element'),
                    mof_elements.count,
                    on='element')

    data.to_csv("subset_data.csv")


if __name__ == "__main__":
    main()
