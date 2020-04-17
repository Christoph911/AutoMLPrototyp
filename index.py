import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from main import app
from apps import app1, app2
from layouts import layout1, layout2
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return layout1
    elif pathname == '/apps/app2':
        return layout2
    else:
        return '404 - Hier gibt es nichts zu sehen!'

if __name__ == '__main__':
    app.run_server(debug=True)
