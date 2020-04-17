import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from main import app
from layouts import layout_unsupervised, layout_supervised
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return layout_supervised
    elif pathname == '/unsupervised':
        return layout_unsupervised
    else:
        return '404 - Hier gibt es nichts zu sehen!'

if __name__ == '__main__':
    app.run_server(debug=True)
