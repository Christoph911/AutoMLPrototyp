import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from main import app
from layouts.masterlayout import layout_start
from callbacks import *
from layouts.layout_upload import layout_upload
from layouts.layout_preprocessing import layout_prep
from layouts.layout_linear_regression import layout_model
from layouts.layout_kmeans import layout_kmeans
from layouts.layout_random_forest import layout_forest


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # hidden Div for storing upload data as json
    html.Div(id='stored-data', style={'display': 'none'}),
    # hidden Div for storing table-prep results as json
    html.Div(id='table-new', style={'display': 'none'}),

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
    elif pathname == '/forest':
        return layout_forest
    elif pathname == '/kmeans':
        return layout_kmeans
    else:
        return '404 - Hier gibt es nichts zu sehen!'


if __name__ == '__main__':
    app.run_server(debug=True)
