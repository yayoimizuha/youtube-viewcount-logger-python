from graph_gen import frame_collector
from pandas import DataFrame

tables: dict = frame_collector()
for key, value in tables.items():
    value: DataFrame = value
    if value.columns.__len__() < 5: continue
    value.dropna(axis=1, how='all',inplace=True)
    print(value.columns[-2:])
    print(value.columns[-3:-1])
    print(value.loc[:, value.columns[-2:]].to_numpy() - value.loc[:, value.columns[-3:-1]].to_numpy())
    value.loc[:, ['today_displace','yesterday_displace']] = \
        value.loc[:, value.columns[-2:]].to_numpy() - value.loc[:, value.columns[-3:-1]].to_numpy()
    # value.loc[:, 'yesterday_displace'] = value.loc[:, value.columns[-2]] - value.loc[:, value.columns[-3]]
    print(value)
    exit()
