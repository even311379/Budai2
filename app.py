import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from layouts import map_layout, env_layout,\
 birds_layout, fish_layout, polychaeta_layout, zooplankton_layout, explain_layout

from setup_app import app
import callbacks

server = app.server

app.layout = html.Div([
    html.H1('布袋鹽田濕地生態調查資料視覺化', className='page-title'),
    dbc.Container([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='說明', children=explain_layout,className='tab',selected_className='tab-selected'),
        dcc.Tab(label='地圖', children=map_layout,className='tab',selected_className='tab-selected'),
        dcc.Tab(label='環境資料', children=env_layout,className='tab',selected_className='tab-selected'),
        dcc.Tab(label='鳥類資料', children=birds_layout,className='tab',selected_className='tab-selected'),
        dcc.Tab(label='魚蝦蟹資料', children=fish_layout,className='tab',selected_className='tab-selected'),
        dcc.Tab(label='多毛類資料', children=polychaeta_layout,className='tab',selected_className='tab-selected'),
        dcc.Tab(label='浮游動物資料', children=zooplankton_layout,className='tab',selected_className='tab-selected'),
    ],className='tabs-container ml-auto',parent_className='tabs'),    
    ]),
    html.Br(),
    html.Br(),
    html.Div(className='footer')
])

if __name__ == '__main__':
    app.run_server(debug=False)
