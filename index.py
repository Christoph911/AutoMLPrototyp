import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from main import app
from Layouts.masterlayout import layout_unsupervised, layout_supervised,layout_start
from Callbacks import *
from Layouts.layoutUpload import layout_upload
from Layouts.layoutPreprocessing import layout_prep
from Layouts.layoutModel import layout_model

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # hidden Div for storing upload data as json
    html.Div(id='stored-data', style={'display': 'none'}),
    # hidden Div for storing table-prep results as json
    html.Div(id='table-new',style={'display': 'none'}),

    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return layout_start
    elif pathname == '/upload':
        return layout_upload
    elif pathname == '/prep':
        return layout_prep
    elif pathname == '/model':
        return layout_model
    elif pathname == '/supervised':
        return layout_supervised
    elif pathname == '/unsupervised':
        return layout_unsupervised
    else:
        return '404 - Hier gibt es nichts zu sehen!'

if __name__ == '__main__':
    app.run_server(debug=True)
