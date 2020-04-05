import base64
import io

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table
from main import app
import pandas as pd

layout = dbc.Container(
    [
        html.H1("SEITE 2"),
        html.Hr(),
        dcc.Upload(
            id="upload-data",
            children=dbc.Button("Datensatz hochladen", color="light")
        ),
        html.Div(id="output-data-upload")
    ]
)


def parse_contents(contents, filename):
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
            'Fehler beim Datei-Upload!'
        ])
    num_col = len(df.columns)
    num_rows = len(df.index)
    num_null = df.isnull().sum().sum()

    return html.Div([
        html.H5("Dateiname: " + filename),
        html.P("Anzahl Spalten: " + str(num_col)),
        html.P("Anzahl Reihen: " + str(num_rows)),
        html.P("Anzahl NaN Values: " + str(num_null)),
        # return dataTable
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
        html.Hr(),

    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        dataframe = parse_contents(list_of_contents, list_of_names)
        return dataframe
