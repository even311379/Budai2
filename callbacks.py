from dash.dependencies import Input, Output

import pandas as pd

from app import app
from my_figs import draw_amount_series, draw_group_bar, draw_env_bar,\
    parse_treemap_input, draw_tree9
from my_stats import get_total_species, get_total_individual,get_most_abundant,\
    get_most_common, get_rarest, get_max_unit, get_total_bird, get_total_bird_counts,\
    get_abundant_bird, get_common_bird


bird_df = pd.read_csv('data/鳥類資料統整201907_mod.csv')
fish_df = pd.read_excel('data/AdditionalData.xlsx',sheet_name = '2018-2019_魚蝦蟹數據')
polychaeta_df = pd.read_excel('data/AdditionalData.xlsx',sheet_name = '2018-2019_多毛類數據').round(2)
zooplankton_df = pd.read_excel('data/AdditionalData.xlsx',sheet_name = '2018-2019_浮游動物數據').round(2)

env_df1 = pd.read_excel('data/AdditionalData.xlsx',sheet_name = '2018-2019_水質儀數據')
env_df2 = pd.read_excel('data/AdditionalData.xlsx',sheet_name = '2018-2019_水質送檢數據')
env_df3 = pd.read_excel('data/AdditionalData.xlsx',sheet_name = '2018-2019_底泥重金屬數據')


# env callbacks
@app.callback(
    [Output('wm-fig1','figure'),
    Output('wm-fig2','figure'),
    Output('wm-fig3','figure'),
    Output('wm-fig4','figure'),
    Output('wm-fig5','figure'),
    Output('wm-fig6','figure'),
    Output('wm-fig7','figure'),
    Output('wm-fig8','figure'),
    Output('wm-fig9','figure'),
    Output('wm-fig10','figure')],
    [Input('WatermeterXmodeSelector', 'value')])
def Update_water_meter(xmode):
    fig1 = draw_env_bar(env_df1,'水溫(℃)',xmode)
    fig2 = draw_env_bar(env_df1,'pH值',xmode)
    fig3 = draw_env_bar(env_df1,'氫離子濃度(mV)',xmode)
    fig4 = draw_env_bar(env_df1,'氧化還原電位(mV)',xmode)
    fig5 = draw_env_bar(env_df1,'導電度(mS/cm)',xmode)
    fig6 = draw_env_bar(env_df1,'濁度(NTU)',xmode)
    fig7 = draw_env_bar(env_df1,'溶氧量(mg/L)',xmode)
    fig8 = draw_env_bar(env_df1,'溶氧度(%)',xmode)
    fig9 = draw_env_bar(env_df1,'總固形物(g/L)',xmode)
    fig10 = draw_env_bar(env_df1,'鹽度(ppt)',xmode)
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10

@app.callback(
    [Output('wl-fig1','figure'),
    Output('wl-fig2','figure'),
    Output('wl-fig3','figure'),
    Output('wl-fig4','figure'),
    Output('wl-fig5','figure'),
    Output('wl-fig6','figure'),
    Output('wl-fig7','figure'),
    Output('wl-fig8','figure'),
    Output('wl-fig9','figure')],
    [Input('WaterlabXmodeSelector', 'value')])
def Update_water_lab(xmode):
    fig1 = draw_env_bar(env_df2,'懸浮固體',xmode,' (mg/L)')
    fig2 = draw_env_bar(env_df2,'含高鹵離子化學需氧量',xmode,' (mg/L)')
    fig3 = draw_env_bar(env_df2,'生化需氧量',xmode,' (mg/L)')
    fig4 = draw_env_bar(env_df2,'氨氮',xmode,' (mg/L)')
    fig5 = draw_env_bar(env_df2,'硝酸鹽氮',xmode,' (mg/L)')
    fig6 = draw_env_bar(env_df2,'亞硝酸鹽氮',xmode,' (mg/L)')
    fig7 = draw_env_bar(env_df2,'凱氏氮',xmode,' (mg/L)')
    fig8 = draw_env_bar(env_df2,'總氮',xmode,' (mg/L)')
    fig9 = draw_env_bar(env_df2,'總磷',xmode,' (mg/L)')
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9

@app.callback(
    [Output('hm-fig1','figure'),
    Output('hm-fig2','figure'),
    Output('hm-fig3','figure'),
    Output('hm-fig4','figure'),
    Output('hm-fig5','figure'),
    Output('hm-fig6','figure'),
    Output('hm-fig7','figure'),
    Output('hm-fig8','figure'),],
    [Input('hmXmodeSelector', 'value')])
def Update_heavy_metal(xmode):
    fig1 = draw_env_bar(env_df3,'鎘',xmode,' (mg/kg)')
    fig2 = draw_env_bar(env_df3,'鎳',xmode,' (mg/kg)')
    fig3 = draw_env_bar(env_df3,'鉻',xmode,' (mg/kg)')
    fig4 = draw_env_bar(env_df3,'鋅',xmode,' (mg/kg)')
    fig5 = draw_env_bar(env_df3,'鉛',xmode,' (mg/kg)')
    fig6 = draw_env_bar(env_df3,'銅',xmode,' (mg/kg)')
    fig7 = draw_env_bar(env_df3,'砷',xmode,' (mg/kg)')
    fig8 = draw_env_bar(env_df3,'汞',xmode,' (mg/kg)')
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8


# bird callbacks
@app.callback(
    [Output('bird-stat0','children'),
    Output('bird-stat1','children'),
    Output('bird-stat2','children'),
    Output('bird-stat3','children')],
    [Input('bird_table','derived_virtual_data')])
def Update_Bird_Stat(rows):
    if rows is None:
        dff = bird_df
    else:
        if len(pd.DataFrame(rows))>0:
            dff = pd.DataFrame(rows)
        else:
            dff = bird_df
    return get_total_bird(dff), get_total_bird_counts(dff),\
    get_abundant_bird(dff), get_common_bird(dff)

@app.callback(
        Output('tree_bird','figure'),
        [Input('bird_table','derived_virtual_data')])
def Update_BirdTree(rows):
    if rows is None:
        dff = bird_df
    else:
        dff = pd.DataFrame(rows)
    
    if len(dff) == 0:
        dff = bird_df
    
    n,exp,v = parse_treemap_input(dff, C='名稱')
    tree = draw_tree9(v,n,exp,title_text = '物種比例')
    
    return tree

@app.callback(
        Output('tree_habitat','figure'),
        [Input('bird_table','derived_virtual_data')])
def Update_HabitatTree(rows):
    if rows is None:
        dff = bird_df
    else:
        dff = pd.DataFrame(rows)
    
    if len(dff) == 0:
        dff = bird_df
        
    n,exp,v = parse_treemap_input(dff, C='棲地')
    tree = draw_tree9(v,n,exp,title_text = '棲地比例')
    
    return tree     

@app.callback(
        Output('tree_family','figure'),
        [Input('bird_table','derived_virtual_data')])
def Update_FamilyTree(rows):
    if rows is None:
        dff = bird_df
    else:
        dff = pd.DataFrame(rows)
    
    if len(dff) == 0:
        dff = bird_df
        
    n,exp,v = parse_treemap_input(dff, C='科名')
    tree = draw_tree9(v,n,exp,title_text = '科別比例')
    
    return tree

@app.callback(
    Output('bs_series','figure'),
    [Input('bird_table','derived_virtual_data'),
     Input('birdUnitSelector', 'value')])
def Update_BS_fig(rows, value):
    if rows is None:
        dff = bird_df
    else:
        dff = pd.DataFrame(rows)
    
    if len(dff) == 0:
        dff = bird_df
        
    bs_fig = draw_amount_series(dff, unit = value)
    
    return bs_fig 

# fish-crab-shirmp callbacks 
@app.callback(
    Output('fish_bar','figure'),
    [Input('fish_table','derived_virtual_data'),
    Input('FishXmodeSelector','value')])
def Update_Fish_bar(rows,xmode):
    if rows is None:
        dff = fish_df
    else:
        if len(pd.DataFrame(rows))>0:
            dff = pd.DataFrame(rows)
        else:
            dff = fish_df
    fish_names = dff.columns.tolist()[3:]
    return draw_group_bar(dff, xmode,fish_names)

@app.callback(
    [Output('fish-stat0','children'),
    Output('fish-stat1','children'),
    Output('fish-stat2','children'),
    Output('fish-stat3','children')],
    [Input('fish_table','derived_virtual_data')]
)
def Update_Fish_Stat(rows):
    if rows is None:
        dff = fish_df
    else:
        if len(pd.DataFrame(rows))>0:
            dff = pd.DataFrame(rows)
        else:
            dff = fish_df
    return get_total_species(dff), get_total_individual(dff),get_most_abundant(dff),\
    get_most_common(dff)


# polychaeta callbacks 
@app.callback(
    Output('polychaeta_bar','figure'),
    [Input('polychaeta_table','derived_virtual_data'),
    Input('polychaetaXmodeSelector','value')])
def Update_polychaeta_bar(rows,xmode):
    if rows is None:
        dff = polychaeta_df
    else:
        if len(pd.DataFrame(rows))>0:
            dff = pd.DataFrame(rows)
        else:
            dff = polychaeta_df
    polychaeta_names = dff.columns.tolist()[3:]
    return draw_group_bar(dff, xmode,polychaeta_names,'多毛類密度 (隻/平方公尺)','mean')

@app.callback(
    [Output('polychaeta-stat0','children'),
    Output('polychaeta-stat1','children'),
    Output('polychaeta-stat2','children'),
    Output('polychaeta-stat3','children')],
    [Input('polychaeta_table','derived_virtual_data')]
)
def Update_polychaeta_Stat(rows):
    if rows is None:
        dff = polychaeta_df
    else:
        if len(pd.DataFrame(rows))>0:
            dff = pd.DataFrame(rows)
        else:
            dff = polychaeta_df
    return get_total_species(dff), get_max_unit(dff), get_most_common(dff),\
        get_rarest(dff)


# zooplankton callbacks 
@app.callback(
    Output('zooplankton_bar','figure'),
    [Input('zooplankton_table','derived_virtual_data'),
    Input('zooplanktonXmodeSelector','value')])
def Update_zooplankton_bar(rows,xmode):
    if rows is None:
        dff = zooplankton_df
    else:
        if len(pd.DataFrame(rows))>0:
            dff = pd.DataFrame(rows)
        else:
            dff = zooplankton_df
    zooplankton_names = dff.columns.tolist()[3:]
    return draw_group_bar(dff, xmode,zooplankton_names,'浮游動物密度 (隻/公升)','mean')

@app.callback(
    [Output('zooplankton-stat0','children'),
    Output('zooplankton-stat1','children'),
    Output('zooplankton-stat2','children'),
    Output('zooplankton-stat3','children')],
    [Input('zooplankton_table','derived_virtual_data')]
)
def Update_zooplankton_Stat(rows):
    if rows is None:
        dff = zooplankton_df
    else:
        if len(pd.DataFrame(rows))>0:
            dff = pd.DataFrame(rows)
        else:
            dff = zooplankton_df
    return get_total_species(dff), get_max_unit(dff,'隻/公升'), get_most_common(dff),\
        get_rarest(dff)