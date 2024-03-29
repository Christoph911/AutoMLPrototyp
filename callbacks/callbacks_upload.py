import base64
import io
import json
from main import app

import dash_table
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import dash_core_components as dcc

pd.options.plotting.backend = "plotly"


# parse uploaded data and return dataframe
def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        df = pd.read_excel(io.BytesIO(decoded))
        print(df)
    elif 'txt' or 'tsv' in filename:
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))

    return df


# convert uploaded data to json and store it in hidden div
@app.callback(
    [Output('stored-data-upload', 'children'),
     Output('error-message-upload', 'children')],
    [Input('upload', 'contents'),
     Input('upload', 'filename')]
)
def upload_data(contents, filename):
    if contents:
        try:
            contents = contents[0]
            filename = filename[0]
            data = parse_data(contents, filename)
            data = data.to_json(orient='split')
            return data, None
        except:
            error_message_upload = dbc.Modal(
                [
                    dbc.ModalHeader("Fehler!"),
                    dbc.ModalBody(["Es ist ein Fehler beim Dateiupload aufgetreten:", html.Br(),
                                   "Bitte stell sicher, dass die hochzuladene Datei im CVS oder"
                                   " einem Excel-Dateiformat vorliegt!"]),
                    dbc.ModalFooter("")
                ],
                is_open=True,
            ),
            return None, error_message_upload


# take stored data, display dash table and some basic statistics
@app.callback(
    Output('table-head', 'children'),
    [Input('stored-data-upload', 'children'),
     Input('card-tabs', 'active_tab')
     ]
)
def display_table(df, active_tab):
    if df is None:
        raise PreventUpdate
    elif df is not None:
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
        infos = html.Div([html.H6('Dataset Shape:'), str(df.shape), html.Br(),
                          html.H6('Anzahal NaN Werte in Spalten:'), str(df.isna().sum()), html.Br(),
                          html.H6('Datentypen der Spalten:'), str(df.dtypes), html.Br()
                          ])
        return infos

    elif active_tab == 'tab-3':
        # get values for corr-matrix
        z = df.corr().round(2).values
        # delete non numeric values
        df_numeric = df._get_numeric_data()
        # get column names for axis
        x = list(df_numeric.columns)
        y = list(df_numeric.columns)
        # create heatmap
        fig = ff.create_annotated_heatmap(z, x=x, y=y, colorscale='Blues')
        fig.update_layout(title_text='Korrelations-Matrix',
                          width=1200,
                          height=800,

                          )

        return dcc.Graph(figure=fig)

    elif active_tab == 'tab-4':
        df_numeric = df._get_numeric_data()
        fig_hist = df_numeric.plot.hist()

        return dcc.Graph(figure=fig_hist)
    else:
        raise PreventUpdate
