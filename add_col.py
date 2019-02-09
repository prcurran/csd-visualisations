from elements import ELEMENTS

import pandas as pd

num = [e.number for e in ELEMENTS]
sym = [e.symbol for e in ELEMENTS]
group = [e.group for e in ELEMENTS]
period = [e.period for e in ELEMENTS]
block = [e.block for e in ELEMENTS]


df = pd.DataFrame({'element':sym,
                   'index':num,
                   'group':group,
                   'period':period,
                   'block':block

                   })


main_df = pd.read_csv("subset_data.csv", index_col=0)




missing = set(df['element'])-set(main_df['element'])

exd = pd.DataFrame({'element': list(missing),
                    'csd': [0] * len(missing),
                    'drug': [0] * len(missing),
                    'mof': [0] * len(missing)})

main_df = main_df.append(exd)
#
print df
print main_df
new =pd.merge(main_df, df, on='element')
#
new.to_csv("extra.csv", index=False)