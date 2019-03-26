import pandas as pd


a = pd.read_csv("pca_data.csv", index_col=0)

b = pd.read_csv("data.csv", index_col=0)

c = a.merge(b, how='left', on='refcode')

c.to_csv("merge.csv")