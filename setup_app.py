import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    external_stylesheets=[dbc.themes.CERULEAN,
    'https://fonts.googleapis.com/css?family=Noto+Sans+TC&display=swap',
    'https://freelancerlife.info/static/css/budai.css'],
    )
app.title = '布袋鹽田生態調查資料'
app.config.suppress_callback_exceptions = True
server = app.server
