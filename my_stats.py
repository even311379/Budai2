import pandas as pd

## for bird stats
def get_total_bird(bdf):
    return len(set(bdf['名稱']))

def get_total_bird_counts(bdf):
    return bdf['數量'].sum()

def get_abundant_bird(bdf):
    tdf = bdf[['名稱','數量']]
    t = tdf.groupby(['名稱']).sum().sort_values(by='數量',ascending=False).數量
    return f'{t.index[0]} ({t[0]}隻)'

def get_common_bird(bdf):
    tdf = bdf[['年','月','樣區','樣站','名稱']]
    t = tdf.groupby(['名稱']).count().iloc[:,0].sort_values(ascending=False) 
    return f'{t.index[0]} ({t[0]}次)'


## for data format in AdditionalData.xlsx
def get_total_species(df):
    n = sum(df.iloc[:,3:].sum()>0)
    return f'{n}種'

def get_total_individual(df):
    n = sum(df.iloc[:,3:].sum())
    return f'{int(n)}隻'

def get_most_abundant(df):
    td = df.iloc[:,3:].sum().sort_values(ascending=False)
    return f'{td.index[0]} ({int(td[0])}隻)'

def get_max_unit(df,unit='隻/平方公尺'):
    td = df.iloc[:,3:].max().sort_values(ascending=False)
    return f'{td[0]} {unit} ({td.index[0]})'

def get_most_common(df):
    td = (df.iloc[:,3:]>0).sum().sort_values(ascending=False) 
    names = [i for v, i in zip(td,td.index) if v == td[0]]
    return f"{','.join(names)} ({td[0]}次)"

def get_rarest(df):
    td = (df.iloc[:,3:]>0).sum().sort_values(ascending=True) 
    names = [i for v, i in zip(td,td.index) if v == td[0]]
    return f"{','.join(names)} ({td[0]}次)"
