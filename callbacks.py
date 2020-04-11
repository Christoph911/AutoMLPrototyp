import base64
import io

from main import app
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd


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
# TODO: Callbacks redundanter code. bessere Lösung?
@app.callback(
    [Output('opt-dropdownX', 'options'),
     Output('opt-dropdownY', 'options')],
    [
        Input('upload', 'contents'),
        Input('upload', 'filename')

    ]
)
def update_date_dropdown(contents, filename):
    optionsX = []
    optionsY = []
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)

        optionsX = [{'label': col, 'value': col} for col in df.columns]
        optionsY = [{'label': col, 'value': col} for col in df.columns]
    return optionsX, optionsY

# TODO: Zwei gleiche Auswahlmögl. ausschließen