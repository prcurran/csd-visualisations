import pandas as pd

import seaborn as sns

sns.set(style="white",
        rc={"axes.facecolor": (0, 0, 0, 0)},
        font_scale=.55)

df = pd.read_csv("extra.csv", index_col=0)


#df['n_csd'] =

# df['csd'] = df['csd'] / sum(df['csd'])
# df['drug'] = df['drug'] / sum(df['drug'])
# df['mof'] = df['mof'] / sum(df['mof'])

organics = set(["H","C","O","N","S","Cl","F","P","I","Br"])
firstrow =set(df.loc[df['period'].isin([1,2,3,7,8])]["element"])
#print firstrow
group1 = set(df["element"]) - organics -firstrow

#group1 = set(df.loc[df['block'] == 'f']["element"])
df = df[df['element'].isin(group1)]

#df = df.drop(index=1)
df = df.drop(['block', 'group', 'period'], 1)


new = pd.melt(df, id_vars='element', var_name='database', value_name='count')
new = new.loc[new['database']=='drug']
print new


plt = sns.barplot(x='element', y='count', data=new, linewidth=1.5, edgecolor=".2", facecolor='Salmon')


plt.set_xlabel("Elements")
plt.set_ylabel("Frequency")
plt.set_title("'Non-Standard' Drugs Atoms")
plt.figure.show()
# ax = sns.catplot(x='element', y='count', hue='database', data=new, kind='bar', palette="Reds", linewidth=1.5,
#                  edgecolor=".2",
#                  legend_out=True)

# ax._legend.set_title("CSD Set")
# new_labels = ["All", "Drug", "MOF"]
# for t, l in zip(ax._legend.texts, new_labels): t.set_text(l)
#
# ax.set_axis_labels(x_var="Elements", y_var="Frequency")
#
# ax.set(title="Frequency of Lanthanoid Elements in the CSD")
# for patch in ax.artists:
#     r, g, b, a = patch.get_facecolor()
#     patch.set_facecolor((r, g, b, .7))

#ax.fig.show()



#ax.set_xlabel()
#ax.figure.show()