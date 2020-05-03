import base64
import io
import json
from main import app

import dash_table
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

# parse uploaded data and return dataframe
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


# convert uploaded data to json and store it in hidden div
@app.callback(
    Output('stored-data-upload', 'children'),
    [Input('upload', 'contents'),
     Input('upload', 'filename')]
)
def store_data(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.to_json(orient='split')
        print("Daten in hidden Div gespeichert")
        return df

# take stored data, display dash table and some basic statistics
@app.callback(
    Output('table-head', 'children'),
    [Input('stored-data-upload', 'children'),
     Input('card-tabs', 'active_tab')
     ]
)
def display_table(df, active_tab):
    if df == None:
        raise PreventUpdate
    elif df != None:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])
        dff = df.head(10)

    if active_tab == 'tab-1':
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in dff.columns],
            data=dff.to_dict('rows'),
            style_cell={'width': '150',
                        'height': '60px',
                        'textAlign': 'left'})

        return table

    elif active_tab == 'tab-2':
        shape = html.P(['Dataset Shape:', html.Br(), str(df.shape), html.Br(),
                        'Anzahal NaN Werte in Spalten:', html.Br(), str(df.isna().sum()), html.Br(),
                        ])
        return shape

    else:
        raise PreventUpdate