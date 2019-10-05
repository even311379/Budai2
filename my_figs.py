# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 13:11:31 2019

@author: DB
"""

import plotly.graph_objects as go
import palettable.cartocolors.qualitative as cartocolors
import textwrap
import squarify
import pandas as pd
import json
import numpy as np
import datetime
import collections

para_names = ['溫度','導電度（mS/cm）','氧化還原電位（mV, ORP）','溶氧量（mg/L, DO）','溶氧度（%）','濁度（NTU）','酸鹼值（pH）','鹽度（ppt）','總固形物（g/L, TDS）','水深']

def get_geoj_poly_cents(geoj_dict):
    c_lat = []
    c_lon = []
    c_name = []
    for A in geoj_dict['features']:
        tc_lat = []
        tc_lon = []
        for i in A['geometry']['coordinates'][0]:
            tc_lat.append(i[1])
            tc_lon.append(i[0])

        c_lat.append(np.mean(tc_lat))
        c_lon.append(np.mean(tc_lon))
        c_name.append(A['properties']['name'])
    return c_lat, c_lon, c_name



def draw_water_bg_map():
    
    mapbox_access_token = 'pk.eyJ1IjoiZXZlbjMxMTM3OSIsImEiOiJjamFydGVtOHk0bHo1MnFyejhneGowaG1sIn0.gyK3haF84TD-oxioghabsQ'
    
    with open('data/sample_sites.json', 'r') as j:
        jf = json.loads(j.read())

    lat = []
    lon = []
    site_id = []
    
    for i in jf['features']:
        lat.append(i['geometry']['coordinates'][1])
        lon.append(i['geometry']['coordinates'][0])
        site_id.append(i['properties']['site'])
    
    with open('data/power_area.geojson', 'r', encoding='utf8') as j:
        pa_gj = json.loads(j.read())
    
    c_lat, c_lon, c_name = get_geoj_poly_cents(pa_gj)
    
    with open('data/power_area.geojson', 'r', encoding='utf8') as j:
        l1 = json.loads(j.read())
    l1['features'].pop(0)
    with open('data/power_area.geojson', 'r', encoding='utf8') as j:
        l2 = json.loads(j.read())
    l2['features'].pop(1)
    
    '''
    this is for annotation, best solution for it so far is to add another scattermapbox
    , the issue is that it will be invisible if overlapped with existing marks, so I fine tune its lat.
    
    https://plot.ly/python/mapbox-layers/#how-layers-work-in-mapbox-maps
    
    must set below="" in order to make mapbox layer insert correctly,
    this layer name is vevy hard to find...
    satellite have no othe layers, so I use satellite-street and below='ferry' make it work!!!
    '''
    data = [
         go.Scattermapbox(
            lat = [c_lat[0] - 0.0002, c_lat[1] + 0.001],
            lon = c_lon,
            mode='text',
            text = c_name,
            hoverinfo = 'text',
            hovertext = '',
            textfont=dict(family='Noto Sans TC', size=14, color='#3a1f5d'),
        ),
        go.Scattermapbox(
            lat=lat,
            lon=lon,
            mode='markers+text',
            marker=dict(
                size=18,
                color='#c83660',
            ),
            text=site_id,
            hoverinfo = 'text',
            hovertext=site_id,
            textfont=dict(family='Noto Sans TC', size=14, color='#ebfffb'),
        ),
       
        ]
    
    layers=([dict(sourcetype = 'geojson',
          source =l1,
          below="ferry",
          type = 'fill',    # the borders
          color = '#f5fec0',
          opacity=0.5
          ),
         dict(sourcetype = 'geojson',
          source =l2,
          below="ferry",
          type = 'fill',    # the borders
          color = '#caf2d7',
          opacity=0.5
          )
        ])
         
    layout = go.Layout(
        title='樣點位置',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Noto Sans TC'),
        autosize=True,
        hovermode='closest',
        # clickmode='event+select',
        # dragmode="lasso",
        clickmode='none',
        dragmode="pan",
        showlegend=False,
        height=500,
        margin=dict(l=0,r=0,b=0,t=30),
        mapbox=dict(
            accesstoken=mapbox_access_token,
            layers=layers,
            bearing=0,
            center=dict(
                lat=23.330677,
                lon=120.184300
            ),
            pitch=0,
            zoom=15,
            style='satellite-streets',
        ),
    )
            
    bg_map = go.Figure(data=data, layout=layout)
    
    return bg_map



def draw_env_bar(df,var_name,x_mode = 0,unit = ''):
    '''
    x_mode:
        0 -> sort by time
        1 -> sort by site
    sort by time or site
    sep with shape
    '''
    if x_mode == 1:
        df = df.sort_values(['樣點編號'])

    sample_id = ['BD80'+str(i) if i < 10 else 'BD8'+str(i) for i in df['樣點編號'].tolist()]
    year = df['年份'].tolist()
    month = df['月份'].tolist()
    if x_mode == 1:
        x = [f'{i} ({j}/{k})' for i,j,k in zip(sample_id,year,month)]        
        u_x = list(collections.OrderedDict.fromkeys(sample_id).keys())
        t = [sample_id.count(i) for i in u_x]
        shp_x = [sum(t[:i]) for i in range(len(t))][1:]
        
    else:
        x = [f'{j}/{k} ({i})' for i,j,k in zip(sample_id,year,month)]
        t_x = [100*i + j for i,j in zip(year,month)]
        u_x = list(collections.OrderedDict.fromkeys(t_x).keys())
        t = [t_x.count(i) for i in u_x]
        shp_x = [sum(t[:i]) for i in range(len(t))][1:]



    y = df[var_name].tolist()
    data = go.Bar(x = x, y=y, width=0.6)
    shps = [go.layout.Shape(type="line",xref="x",yref="paper", x0 = s-0.5, y0 = -1, x1 =s-0.5,y1 = 1,line=dict(width=1.5,color="Crimson")) for s in shp_x]
    layout = go.Layout(
        height=200,
        width=500,
        title=var_name + unit,
        xaxis=dict(tickangle=90,tickfont=dict(size=8)),
        shapes=shps,
        hovermode="x",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Noto Sans TC'),
        margin=dict(l=0,r=0,b=0,t=50),
    )
    return go.Figure(data=data,layout=layout)

def draw_bird_sample_map():
    mapbox_access_token = 'pk.eyJ1IjoiZXZlbjMxMTM3OSIsImEiOiJjamFydGVtOHk0bHo1MnFyejhneGowaG1sIn0.gyK3haF84TD-oxioghabsQ'
    
    with open('data/birds_site.geojson', 'r', encoding='utf8') as j:
        bs_gj = json.loads(j.read())
        
    c_lat, c_lon, c_name = get_geoj_poly_cents(bs_gj)
    
    data = [go.Scattermapbox(
                lat = c_lat,
                lon = c_lon,
                mode='markers+text',
                marker=dict(
                    size=24,
                    color='#c83660',
                ),
                text = c_name,
                hoverinfo = 'text',
                hovertext = '',
                textfont=dict(family='Noto Sans TC', size=14, color='#ebfffb'),
            )]
    src = []

    with open('data/birds_site.geojson', 'r', encoding='utf8') as j:
        bs_gj = json.loads(j.read())
    
    for i in bs_gj['features']:
        t = bs_gj.copy()
        t['features'] = [i]
        src.append(t)
    
    layers=([dict(sourcetype = 'geojson',
                  source =t,
                  below="ferry",
                  type = 'fill',    # the borders
                  color = t['features'][0]['properties']['fill'],
                  opacity=0.8
                  ) for t in src])
    
    layout = go.Layout(
            title='鳥類調查範圍',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Noto Sans TC'),
            autosize=True,
            hovermode='closest',
            clickmode='none',
            dragmode="pan",
            showlegend=False,
            height=500,
            margin=dict(l=0,r=0,b=0,t=30),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                layers=layers,
                bearing=0,
                center=dict(
                    lat=23.330677,
                    lon=120.184300
                ),
                pitch=0,
                zoom=15,
                style='satellite-streets',
            ),
        )
    
    bs_map = go.Figure(data=data, layout=layout)
    return bs_map    
        
def parse_treemap_input(df, C = '名稱'):
    name = []
    N = []
    p = []
    for i in df[C].unique():
        name.append(i)
        n = df[df[C] == i]['數量'].sum()
        N.append(n)
        p.append(round(n*100/df['數量'].sum(),2))

    tdf = pd.DataFrame([name, N ,p]).T
    tdf.columns = ['Name', 'Total', 'Percent']
    tdf.sort_values('Percent',ascending=False,inplace=True)
    tdf.reset_index(drop=True,inplace=True)

    if len(tdf) > 8:
        o_names = tdf[:8].Name.tolist() + ['其他']
        o_exp = [f'{n}: {p}%, N = {t}' for n, p,t in zip(tdf[:8].Name,tdf[:8].Percent,tdf[:8].Total)]
        sl = tdf[8:].Name.tolist()
        k = round(tdf[8:].Percent.sum(),2)
        if len(sl) > 10:
            n_left = len(tdf) - 18
            o_exp.append('<br>'.join(textwrap.wrap(f'{k}%, 包含: {sl[:10]} ... 及其他{n_left}種',30)))
        else:
            o_exp.append('<br>'.join(textwrap.wrap(f'{k}%, 包含: {sl[:10]}',30)))
        o_v = tdf[:8].Percent.tolist() + [k]
    else:
        o_names = tdf[:8].Name.tolist()
        o_exp = [f'{n}: {p}%, N = {t}' for n, p,t in zip(tdf[:8].Name,tdf[:8].Percent,tdf[:8].Total)]
        o_v = tdf[:8].Percent.tolist()

    return o_names, o_exp, o_v

def draw_tree9(vs, n, exp, title_text):
    fig = go.Figure()

    x = 0.
    y = 0.
    width = 100.
    height = 100.

    values = vs
    names = n

    normed = squarify.normalize_sizes(values, width, height)
    rects = squarify.squarify(normed, x, y, width, height)

    # Choose colors from http://colorbrewer2.org/ under "Export"
    color_brewer = cartocolors.Prism_9.hex_colors

    shapes = []
    annotations = []
    
    m_names = [nn if vv > 0.5 else '' for nn,vv in zip(names,values)]

    for r, val, color, n in zip(rects, values, color_brewer, m_names):
        shapes.append(
            dict(
                type = 'rect',
                x0 = r['x'],
                y0 = r['y'],
                x1 = r['x']+r['dx'],
                y1 = r['y']+r['dy'],
                line = dict( width = 2 ),
                fillcolor = color
            )
        )
        annotations.append(
            dict(
                x = r['x']+(r['dx']/2),
                y = r['y']+(r['dy']/2),
                text = n,
                showarrow = False,
                font = dict(size=18, color='#ebfffb',family='Noto Sans TC')
            )
        )

    # For hover text
    fig.add_trace(go.Scatter(
        x = [ r['x']+(r['dx']/2) for r in rects ],
        y = [ r['y']+(r['dy']/2) for r in rects ],
        text = exp,
        mode = 'text',
        hoverinfo='text',
        textfont = dict(size=16, color='#ebfffb',family='Noto Sans TC'),
    ))

    fig.update_layout(
        title=title_text,
        #width=500,
        #height=500,
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
        shapes=shapes,
        annotations=annotations,
        hovermode='closest',
        dragmode=False,
        # margin=dict(l=10,r=10,b=10,t=10),
        margin=dict(l=0,r=0,b=0,t=50),
        # plot_bgcolor='#ebfffb',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Noto Sans TC')
    #     paper_bgcolor="#00ff00",
    )
    
#    fig.update_xaxes()
#    fig.update_yaxes(showticklabels=False)
    
    return fig

def draw_amount_series(df, unit = '樣區'):
    g = df.groupby(['年','月',unit]).sum()
    Y = g.index.get_level_values(0).tolist()
    M = g.index.get_level_values(1).tolist()
    U = g.index.get_level_values(2).tolist()
    D = [datetime.datetime(year=y, month=m, day=15) for y, m in zip(Y,M)]
    V = g['數量'].tolist()
    
    data = []
    
    for u in set(U):
        ind = [i for i,v in enumerate(U) if v == u]
        X = [D[i] for i in ind]
        Y = [V[i] for i in ind]
        data.append(go.Scatter(x = X, y = Y, name = f'{unit}: {u}'))
    
    layout = go.Layout(
        title='鳥類總數量',
        legend=dict(bgcolor="rgba(0,0,0,0)",bordercolor="Black",borderwidth=2),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Noto Sans TC'),
        hovermode="x",
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

def draw_group_bar(df, xmode, y_targets,title_text='魚蝦蟹類隻數', stat='sum'):
    if xmode == 0:
        if stat == 'sum':
            ndf = df.groupby(['樣點編號']).sum()
        elif stat == 'mean':
            ndf = df.groupby(['樣點編號']).mean()
        x = ['BD80'+str(i) if i < 10 else 'BD8'+str(i) for i in ndf.index.tolist()]
    elif xmode == 1:
        ndf = df.groupby(['年份','月份']).sum()
        x = [f'{i[0]}/{i[1]}' for i in ndf.index]

    
    data = []
    for target in y_targets:
        data.append(go.Bar(name = target,x=x,y=ndf[target].tolist()))
    layout = go.Layout(
        barmode = 'stack',
        title= title_text,
        legend = dict(bgcolor="rgba(0,0,0,0)",bordercolor="Black",borderwidth=2),
        hovermode="x",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Noto Sans TC')
    )

    fig = go.Figure(data=data,layout=layout)
    return fig

