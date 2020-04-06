import base64
import io

from main import app
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go

import pandas as pd

# define color for scatter plot
colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

# define page layout
layout = dbc.Container(
    [
        html.Div([
            html.H1("Seite 2"),
            html.Hr(),
            # create dcc.Upload inside a button
            dcc.Upload(
                id='upload-data',
                children=dbc.Button("Datensatz hochladen", color="light"),
                multiple=True
            ),
            # place scatter plot and table on layout
            dcc.Graph(id='Mygraph'),
            html.Div(id='output-data-upload')
        ])
    ])

# method reads file, parse it and store as df
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

# callback for scatter plot
@app.callback(Output('Mygraph', 'figure'),
              [
                  Input('upload-data', 'contents'),
                  Input('upload-data', 'filename')
              ])
# creates scatter plot TODO: place values for x and y dynamically
def update_graph(contents, filename):
    x = []
    y = []
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        # df = df.set_index(df.columns[0])
        x = []
        y = []
    fig = go.Figure(
        data=[
            go.Scatter(
                x=x,
                y=y,
                mode="lines+markers"
            )
        ],
        layout=go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    )

    return fig

# callback for table
@app.callback(Output('output-data-upload', 'children'),
              [
                  Input('upload-data', 'contents'),
                  Input('upload-data', 'filename')
              ])
# creates table and some basic information about dataset
def update_table(contents, filename):
    table = html.Div()

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        num_columns = len(df.columns)
        num_rows = len(df.index)
        num_null = df.isnull().sum().sum()

        table = html.Div([
            html.H5("Dateiname: " + filename),
            html.P("Anzahl Spalten: " + str(num_rows)),
            html.P("Anzahl Reihen: " + str(num_columns)),
            html.P("Anzahl Null Values: " + str(num_null)),
            dash_table.DataTable(
                data=df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            ),
            html.Hr(),
        ])

    return table
