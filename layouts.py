import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc

from textwrap import dedent
import pandas as pd

from my_figs import draw_water_bg_map, draw_bird_sample_map, draw_amount_series,\
    draw_tree9, parse_treemap_input, draw_group_bar, draw_env_bar

from my_stats import get_total_species, get_total_individual,get_most_abundant,\
    get_most_common, get_rarest, get_max_unit, get_total_bird, get_total_bird_counts,\
    get_abundant_bird, get_common_bird

## init section
bird_df = pd.read_csv('data/鳥類資料統整201907_mod.csv')
bseries_fig = draw_amount_series(bird_df, '樣區')

n,exp,v = parse_treemap_input(bird_df, C='名稱',)
tree_bird = draw_tree9(v,n,exp,title_text = '物種比例')

n,exp,v = parse_treemap_input(bird_df, C='棲地')
tree_habitat = draw_tree9(v,n,exp,title_text = '棲地比例')

n,exp,v = parse_treemap_input(bird_df, C='科名')
tree_family = draw_tree9(v,n,exp,title_text = '科別比例')

explain_layout = [
    html.Hr(),
    html.H1('這是說明頁面'),
    html.P('之後將會用計畫相關的說明文稿取代這一個頁面'),
    html.Hr(),
    html.H3('Dear Customers:'),
    dcc.Markdown(dedent('''

    這個app的主旨在於**呈現資料**，也因此我讓他盡可能地看起來每個分頁像是專業的報表，
    由於內容過於龐大，不適合用單一page去呈現所有資料，我改以tab的方式呈現包含:**說明**、
    **地圖**、**環境資料**、**鳥類資料**、**魚蝦蟹資料**、**多毛類資料**、**浮游動物資料**等內容。環境資料內又
    再以tab區隔開**水質儀數據**、**水質送檢數據**、**底泥重金屬數據**。

    * 資料表的篩選操作說明:
                    
            1. 在每個欄位名稱的左邊有兩個三角，點選後可以讓資料表依此欄位昇序或降序排列。
                    
            2. 第二列為各欄位的篩選條件，可以直接輸入條件，數值型欄位需使用比較符號(>、<、=)，如`= 2018`、` > 100`;類別型欄位直接輸入數值
            如:`小白鷺`，或部分文字，如:在名稱的篩選條件只輸入`小`，則會將名稱有小的都抓出來。
                    
            3. 如果沒有符合的篩選條件，則資料表會是空白，此時對應到的圖表會是改以依據沒有任何篩選條件的完整數據呈現。

    * 規格

        以瀏覽器寬度1280px進行設計。
    
    * 功能變動

        移除圈選地圖點位來更新圖表的功能

    * 部屬方法:

        此app開發語言為python3，框架為plotly-dash，是基於python的**flask**架構延伸的框架，只需要以一般flask的方式即可佈署上去。
        內建的port為8050，只需要進行**反向代理**(相關程式如nginx、apache)，將這個port接到您想要的url上，即可部屬此app

        我會提供原始碼github給你們部屬。

    #### 我的聯絡方式
    * email: even311379@hotmail.com
    * phone: 0989914039
    * 個人網站： [PUF studio](https://freelancerlife.info)

    #####更新日期 2019/10/06
    
    '''),style={'padding':'1rem 3rem'}),
]


## starts for individual layouts
map_layout = [
    html.Hr(),
    dbc.Row([
        dbc.Col(html.Div([
            dcc.Graph(id='point_map',figure=draw_water_bg_map()),
        ], className='pretty-container'), width=6),
        dbc.Col(html.Div([
            dcc.Graph(id='region_map',figure=draw_bird_sample_map())
        ], className='pretty-container'), width=6),        
    ])
]


env_df1 = pd.read_excel('data/AdditionalData.xlsx',sheet_name = '2018-2019_水質儀數據')
env_df2 = pd.read_excel('data/AdditionalData.xlsx',sheet_name = '2018-2019_水質送檢數據')
env_df3 = pd.read_excel('data/AdditionalData.xlsx',sheet_name = '2018-2019_底泥重金屬數據')

#水質儀數據
wm_layout = html.Div([
    html.H3('水質儀數據'),
    dbc.Row([
        dbc.Col(html.Div('X軸順序:',style={'text-align':'right'}),width=3,className="align-self-center"),
        dbc.Col(dcc.Dropdown(
            id='WatermeterXmodeSelector',
            options = [
                {'label':'時間','value':0},
                {'label':'樣站','value':1},
            ],
            value=0,
            multi=False,
            placeholder="日期?  樣站?"
        ),width=3)
    ],className='justify-content-end'),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df1,'水溫(℃)',0),id='wm-fig1'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df1,'pH值',0),id='wm-fig2'),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df1,'氫離子濃度(mV)',0),id='wm-fig3'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df1,'氧化還原電位(mV)',0),id='wm-fig4'),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df1,'導電度(mS/cm)',0),id='wm-fig5'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df1,'濁度(NTU)',0),id='wm-fig6'),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df1,'溶氧量(mg/L)',0),id='wm-fig7'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df1,'溶氧度(%)',0),id='wm-fig8'),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df1,'總固形物(g/L)',0),id='wm-fig9'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df1,'鹽度(ppt)',0),id='wm-fig10'),width=6)
    ]),
],className='pretty-container')

#水質送檢數據
wl_layout = html.Div([
    html.H3('水質送檢數據'),
    dbc.Row([
        dbc.Col(html.Div('X軸順序:',style={'text-align':'right'}),width=3,className="align-self-center"),
        dbc.Col(dcc.Dropdown(
            id='WaterlabXmodeSelector',
            options = [
                {'label':'時間','value':0},
                {'label':'樣站','value':1},
            ],
            value=0,
            multi=False,
            placeholder="日期?  樣站?"
        ),width=3)
    ],className='justify-content-end'),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df2,'懸浮固體',0,' (mg/L)'),id='wl-fig1'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df2,'含高鹵離子化學需氧量',0,' (mg/L)'),id='wl-fig2'),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df2,'生化需氧量',0,' (mg/L)'),id='wl-fig3'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df2,'氨氮',0,' (mg/L)'),id='wl-fig4'),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df2,'硝酸鹽氮',0,' (mg/L)'),id='wl-fig5'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df2,'亞硝酸鹽氮',0,' (mg/L)'),id='wl-fig6'),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df2,'凱氏氮',0,' (mg/L)'),id='wl-fig7'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df2,'總氮',0,' (mg/L)'),id='wl-fig8'),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df2,'總磷',0,' (mg/L)'),id='wl-fig9'),width=6),            
    ]),
],className='pretty-container')


#底泥重金屬
hm_layout = html.Div([
    html.H3('底泥重金屬'),
    dbc.Row([
        dbc.Col(html.Div('X軸順序:',style={'text-align':'right'}),width=3,className="align-self-center"),
        dbc.Col(dcc.Dropdown(
            id='hmXmodeSelector',
            options = [
                {'label':'時間','value':0},
                {'label':'樣站','value':1},
            ],
            value=0,
            multi=False,
            placeholder="日期?  樣站?"
        ),width=3)
    ],className='justify-content-end'),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df3,'鎘',0,' (mg/kg)'),id='hm-fig1'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df3,'鎳',0,' (mg/kg)'),id='hm-fig2'),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df3,'鉻',0,' (mg/kg)'),id='hm-fig3'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df3,'鋅',0,' (mg/kg)'),id='hm-fig4'),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df3,'鉛',0,' (mg/kg)'),id='hm-fig5'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df3,'銅',0,' (mg/kg)'),id='hm-fig6'),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df3,'砷',0,' (mg/kg)'),id='hm-fig7'),width=6),
        dbc.Col(dcc.Graph(figure=draw_env_bar(env_df3,'汞',0,' (mg/kg)'),id='hm-fig8'),width=6)
    ]),
],className='pretty-container')

env_layout = [
    html.Hr(),
    dcc.Tabs(id="w_tabs", children=[
        dcc.Tab(label='水質儀數據', children=wm_layout,className='tab',selected_className='tab-selected'),
        dcc.Tab(label='水質送檢數據', children=wl_layout,className='tab',selected_className='tab-selected'),
        dcc.Tab(label='底泥重金屬', children=hm_layout,className='tab',selected_className='tab-selected'),
    ],className='wtabs-container ml-auto')
]


birds_layout = [
    html.Hr(),
    dbc.Row([
        dbc.Col([html.Div([
            html.Div([
                html.P('已知物種數:'),
                html.P(get_total_bird(bird_df),id='bird-stat0',className='stats-block')
            ],className='pretty-container'),
            html.Div([
                html.P('總調查隻數:'),
                html.P(get_total_bird_counts(bird_df),id='bird-stat1',className='stats-block')
            ],className='pretty-container'),
            html.Div([
                html.P('總隻數最多: '),
                html.P(get_abundant_bird(bird_df),id='bird-stat2',className='stats-block')
            ],className='pretty-container'),
            html.Div([
                html.P('出現次數最多:'),
                html.P(get_common_bird(bird_df),id='bird-stat3',className='stats-block')
            ],className='pretty-container'),
        ],className='vertical-stack'),],style={'height':'530px'},width=3),
        dbc.Col(html.Div([
            dash_table.DataTable(
                id='bird_table',
                data = bird_df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in bird_df.columns],
                fixed_rows={ 'headers': True, 'data': 0 },
                style_as_list_view=True,
                filter_action='native',
                sort_action='native',
                page_action='none',
                style_cell={
                    'minWidth': '30px',
                    'width': '30px',
                    'maxWidth': '30px'
                },
                style_data={
                    'font-size':'12px',
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'textAlign': 'center'
                },
                style_header={
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'fontWeight': 'bold',
                    'font-size':'14px',
                    'height': 'auto',
                    'minWidth': '0px', 'maxWidth': '50px',
                    'whiteSpace': 'normal',
                    'writing-mode': 'vertical-lr',
                    'transform': 'translateX(30%)',
                    'vertical-align': 'super',
                },
                style_table={
                    'height':'500px'
                }
            ),
        ],className='pretty-container',style={'height':'530px'}),width=9),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='tree_bird', figure=tree_bird, config=dict(displayModeBar=False),style={'height':'300px'})
        ],width=4),
        dbc.Col([
            dcc.Graph(id='tree_habitat', figure=tree_habitat, config=dict(displayModeBar=False),style={'height':'300px'})
        ],width=4),
        dbc.Col([
            dcc.Graph(id='tree_family', figure=tree_family, config=dict(displayModeBar=False),style={'height':'300px'})
        ],width=4),
    ],className='pretty-container'),
    html.Div([
        dcc.Graph(figure=bseries_fig,id='bs_series'),
        dbc.Row([
            dbc.Col(html.Div('繪圖單位:',style={'text-align':'right'}),width=3,className="align-self-center"),
            dbc.Col([
                html.P('選擇分類單位'),
                dcc.Dropdown(
                        id = 'birdUnitSelector',
                        options=[
                            {'label': '樣區', 'value': '樣區'},
                            {'label': '樣站', 'value': '樣站'},
                            {'label': '物種', 'value': '名稱'},
                            {'label': '棲地', 'value': '棲地'},
                            {'label': '科名', 'value': '科名'},
                        ],
                        value='樣區',
                        multi=False,
                        placeholder="選擇分類單位"),
            ],width=3)
        ],className='justify-content-center'),
    ],className='pretty-container')
]


fish_df = pd.read_excel('data/AdditionalData.xlsx',sheet_name = '2018-2019_魚蝦蟹數據')
fish_names = fish_df.columns[3:].tolist()
fish_layout = [
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.Div([
            html.Div([
                html.P('已知物種數:'),
                html.P(get_total_species(fish_df),id='fish-stat0',className='stats-block')
            ],className='pretty-container'),
            html.Div([
                html.P('總捕獲隻數:'),
                html.P(get_total_individual(fish_df),id='fish-stat1',className='stats-block')
            ],className='pretty-container'),
            html.Div([
                html.P('總隻數最多: '),
                html.P(get_most_abundant(fish_df),id='fish-stat2',className='stats-block')
            ],className='pretty-container'),
            html.Div([
                html.P('出現次數最多:'),
                html.P(get_most_common(fish_df),id='fish-stat3',className='stats-block')
            ],className='pretty-container'),
            ],className='vertical-stack'),
        ],style={'height':'530px'},width=3),
        dbc.Col(html.Div([
            dash_table.DataTable(
                id='fish_table',
                data = fish_df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in fish_df.columns],
                fixed_rows={ 'headers': True, 'data': 0 },
                # fixed_columns={'headers':True,'data':3},
                style_as_list_view=True,
                filter_action='native',
                sort_action='native',
                style_cell={
                    'minWidth': '30px',
                    'width': '30px',
                    'maxWidth': '30px'
                },
                style_data={
                    'font-size':'12px',
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'textAlign': 'center'
                },
                style_header={
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'fontWeight': 'bold',
                    'font-size':'14px',
                    'height': 'auto',
                    'minWidth': '0px', 'maxWidth': '50px',
                    'whiteSpace': 'normal',
                    'writing-mode': 'vertical-lr',
                    'transform': 'translateX(30%)',
                    'vertical-align': 'super',
                },
                style_table={
                    'height':'500px'
                }
            ),
        ],className='pretty-container',style={'height':'530px'}),width=9),
    ]),
    html.Div([
        dcc.Graph(figure=draw_group_bar(fish_df,0,fish_df.columns[3:7].tolist()),id='fish_bar'),
        dbc.Row([
            dbc.Col(html.Div('X軸單位:',style={'text-align':'right'}),width=3,className="align-self-center"),
            dbc.Col(
            dcc.Dropdown(
                id = 'FishXmodeSelector',
                options=[
                    {'label': '樣站', 'value': 0},
                    {'label': '時間', 'value': 1},
                ],
                value=0,
                multi=False,
                placeholder="X軸類別",
            ),width=3)
        ],className='justify-content-center'),
    ], className='pretty-container')
]


polychaeta_df = pd.read_excel('data/AdditionalData.xlsx',sheet_name = '2018-2019_多毛類數據').round(2)
polychaeta_names = polychaeta_df.columns[3:].tolist()
polychaeta_layout = [
    html.Hr(),
    dbc.Row([
        dbc.Col([html.Div([
            html.Div([
                html.P('已知物種數:'),
                html.P(get_total_species(polychaeta_df),id='polychaeta-stat0',className='stats-block')
            ],className='pretty-container'),
            html.Div([
                html.P('密度最高:'),
                html.P(get_max_unit(polychaeta_df),id='polychaeta-stat1',className='stats-block')
            ],className='pretty-container'),
            html.Div([
                html.P('出現次數最多:'),
                html.P(get_most_common(polychaeta_df),id='polychaeta-stat2',className='stats-block')
            ],className='pretty-container'),
            html.Div([
                html.P('出現次數最少:'),
                html.P(get_rarest(polychaeta_df),id='polychaeta-stat3',className='stats-block')
            ],className='pretty-container'),
        ],className='vertical-stack'),],style={'height':'530px'},width=3),
        dbc.Col(html.Div([
            dash_table.DataTable(
                id='polychaeta_table',
                data = polychaeta_df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in polychaeta_df.columns],
                fixed_rows={ 'headers': True, 'data': 0 },
                style_as_list_view=True,
                filter_action='native',
                sort_action='native',
                style_cell={
                    'minWidth': '30px',
                    'width': '30px',
                    'maxWidth': '30px'
                },
                style_data={
                    'font-size':'12px',
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'textAlign': 'center'
                },
                style_header={
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'fontWeight': 'bold',
                    'font-size':'14px',
                    'height': 'auto',
                    'minWidth': '0px', 'maxWidth': '50px',
                    'whiteSpace': 'normal',
                    'writing-mode': 'vertical-lr',
                    'transform': 'translateX(30%)',
                    'vertical-align': 'super',
                },
                style_table={
                    'height':'500px'
                }
            ),
        ],className='pretty-container',style={'height':'530px'}),width=9),
    ]),
    html.Div([
        dcc.Graph(figure=draw_group_bar(polychaeta_df,0,polychaeta_names[:4],'多毛類密度 (隻/平方公尺)','mean'),id='polychaeta_bar'),
        dbc.Row([
            dbc.Col(html.Div('X軸單位:',style={'text-align':'right'}),width=3,className="align-self-center"),
            dbc.Col(
                dcc.Dropdown(
                id = 'polychaetaXmodeSelector',
                options=[
                    {'label': '樣站', 'value': 0},
                    {'label': '時間', 'value': 1},
                ],
                value=0,
                multi=False,
                placeholder="X軸類別",
            ),width=3)
        ],className='justify-content-center'),
    ],className='pretty-container')
]

zooplankton_df = pd.read_excel('data/AdditionalData.xlsx',sheet_name = '2018-2019_浮游動物數據')
zooplankton_names = zooplankton_df.columns[3:].tolist()
zooplankton_layout = [
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.Div([
            html.Div([
                html.P('已知物種數:'),
                html.P(get_total_species(zooplankton_df),id='zooplankton-stat0',className='stats-block')
            ],className='pretty-container'),
            html.Div([
                html.P('密度最高:'),
                html.P(get_max_unit(zooplankton_df,'隻/公升'),id='zooplankton-stat1',className='stats-block')
            ],className='pretty-container'),
            html.Div([
                html.P('出現次數最多:'),
                html.P(get_most_common(zooplankton_df),id='zooplankton-stat2',className='stats-block')
            ],className='pretty-container'),
            html.Div([
                html.P('出現次數最少:'),
                html.P(get_rarest(zooplankton_df),id='zooplankton-stat3',className='stats-block')
            ],className='pretty-container'),
            ],className='vertical-stack'),
        ],style={'height':'530px'},width=3),
        dbc.Col(html.Div([
            dash_table.DataTable(
                id='zooplankton_table',
                data = zooplankton_df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in zooplankton_df.columns],
                fixed_rows={ 'headers': True, 'data': 0 },
                style_as_list_view=True,
                filter_action='native',
                sort_action='native',
                style_cell={
                    'minWidth': '30px',
                    'width': '30px',
                    'maxWidth': '30px'
                },
                style_data={
                    'font-size':'12px',
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'textAlign': 'center'
                },
                style_header={
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'fontWeight': 'bold',
                    'font-size':'14px',
                    'height': 'auto',
                    'minWidth': '0px', 'maxWidth': '50px',
                    'whiteSpace': 'normal',
                    'writing-mode': 'vertical-lr',
                    'transform': 'translateX(30%)',
                    'vertical-align': 'super',
                },
                style_table={
                    'height':'500px'
                }
            ),
        ],className='pretty-container',style={'height':'530px'}),width=9),
    ]),
    html.Div([
        dcc.Graph(figure=draw_group_bar(zooplankton_df,0,zooplankton_names[:4],'浮游動物密度 (隻/公升)','mean'),id='zooplankton_bar'),
        dbc.Row([
            dbc.Col(html.Div('X軸單位:',style={'text-align':'right'}),width=3,className="align-self-center"),
            dbc.Col(
            dcc.Dropdown(
                id = 'zooplanktonXmodeSelector',
                options=[
                    {'label': '樣站', 'value': 0},
                    {'label': '時間', 'value': 1},
                ],
                value=0,
                multi=False,
                placeholder="X軸類別",
            ),width=3)
        ],className='justify-content-center'),
    ],className='pretty-container')
]
