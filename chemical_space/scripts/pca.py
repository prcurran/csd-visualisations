import pandas as pd
import numpy as np

from sklearn.feature_selection import VarianceThreshold
from sklearn import decomposition

from rdkit import Chem
from rdkit.Chem import AllChem

from concurrent import futures


def morgan_array(mol):
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024).ToBitString()
    return [int(f) for f in fp]


def get_fps(inputs):

    try:
        refcode, smiles = inputs
        mol = Chem.MolFromSmiles(smiles)
        AllChem.Compute2DCoords(mol)
        fp = morgan_array(mol)

        return [fp, refcode]
    except:
        return [None, refcode]


def main():

    df = pd.read_csv("data.csv").dropna()

    inputs = zip(list(df['refcode']), list(df['smiles']))
    print len(inputs)
    with futures.ProcessPoolExecutor(max_workers=7) as executor:
        a = [i for i in executor.map(get_fps, inputs) if i[0] is not None]
        print len(a)

    fps, refcodes = zip(*a)
    X = np.array(fps)
    cutoff = 0.999
    sel = VarianceThreshold(threshold=(cutoff * (1 - cutoff)))
    X2 = sel.fit_transform(X)
    pca = decomposition.IncrementalPCA(n_components=3, batch_size=50000)
    X_pca = pca.fit_transform(X2)  # Dense data required

    print X_pca.explained_variance_

    x = X_pca[:, 0]
    y = X_pca[:, 1]

    out_df = pd.DataFrame({"x": x,
                           "y": y,
                           "refcode": refcodes})

    out_df.to_csv("pca_data_3d.csv")


if __name__ == '__main__':
    main()



