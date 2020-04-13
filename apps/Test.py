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
from dash.exceptions import PreventUpdate
from sklearn.cluster import KMeans

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
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


# output clustering

@app.callback(
    Output("cluster-graph", "figure"),
    [Input('button', 'n_clicks')],

    [State("opt-dropdownX", "value"),
     State("opt-dropdownY", "value"),
     State("cluster-count", "value"),
     State('upload', 'contents'),
     State('upload', 'filename')
     ],
)
def make_graph(n_clicks, x, y, n_clusters, contents, filename):
    layout = None
    if contents is None or filename is None or x is None or y is None or n_clusters is None:
        raise PreventUpdate

    if contents:
        contents = contents[0]
        filename = filename[0]
        contents = parse_data(contents, filename)

        # minimal input validation, make sure there's at least one cluster
        km = KMeans(n_clusters=max(n_clusters, 1))
        df = contents.loc[:, [x, y]]
        km.fit(df.values)
        df["cluster"] = km.labels_

        centers = km.cluster_centers_

        data = [
            go.Scatter(
                x=df.loc[df.cluster == c, x],
                y=df.loc[df.cluster == c, y],
                mode="markers",
                marker={"size": 8},
                name="Cluster {}".format(c),
            )
            for c in range(n_clusters)
        ]

        data.append(
            go.Scatter(
                x=centers[:, 0],
                y=centers[:, 1],
                mode="markers",
                marker={"color": "#000", "size": 12, "symbol": "diamond"},
                name="Cluster centers",
            )
        )

        layout = {"xaxis": {"title": x}, "yaxis": {"title": y}}

    return go.Figure(data=data, layout=layout)


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
                    options=[
                        {'label': '', 'value': ''}
                    ],
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="opt-dropdownY",
                    options=[
                        {'label': '', 'value': ''}
                    ],
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Anzahl Cluster"),
                dbc.Input(id="cluster-count", type="number", value=3),
            ]
        ),
        html.Button('Click Me', id='button'),
        dcc.Graph(id="cluster-graph"),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
