import base64
import io

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go

import pandas as pd


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

# import dataset
def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'Fehler beim Dateiupload!'
        ])
    return df
# dropdown options
@app.callback(Output('opt-dropdown', 'options'),
    [
        Input('upload', 'contents'),
        Input('upload', 'filename')

    ]
)
def update_date_dropdown(contents,filename):
    options = []
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents,filename)

        options = [{'label': col, 'value': col} for col in df.columns]
    return options

@app.callback(Output('opt-dropdownX', 'options'),
    [
        Input('upload', 'contents'),
        Input('upload', 'filename')

    ]
)
def update_date_dropdownX(contents,filename):
    optionsX = []
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents,filename)

        optionsX = [{'label': col, 'value': col} for col in df.columns]
    return optionsX

# output clustering

# masterlayout
app.layout = html.Div(
    [
        dcc.Upload(
            id="upload",
            children=dbc.Button("hochladen"),
            multiple=True
        ),
        dbc.FormGroup(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="opt-dropdownX",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="opt-dropdown",
                ),
            ]
        ),
        #dcc.Graph("figure")
    ]
)




if __name__ == '__main__':
    app.run_server(debug=True)
