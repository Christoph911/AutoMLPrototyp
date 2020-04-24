import base64
import io
import json
from main import app

import dash_table
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objs as go

import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans


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
    Output('stored-data', 'children'),
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


# take stored data and make some basic preparations
@app.callback(
    Output('data-prepared', 'children'),
    [Input('stored-data', 'children'),
     Input('remove-NaN', 'n_clicks')
     ]
)
def prepare_data(df, n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])
        df = df.dropna()

        return print("Null values entfernt")
    else:
        raise PreventUpdate


# take stored data, display dash table and some basic statistics
@app.callback(
    Output('table-head', 'children'),
    [Input('stored-data', 'children'),
     Input("card-tabs", "active_tab"),
     Input("start-preprocessing", "n_clicks")

     ]
)
def display_table(df, active_tab, n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    elif n_clicks is not None:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])
        dff = df.head(10)

    if active_tab == "tab-1":
        table = dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in dff.columns],
            data=dff.to_dict("rows"),
            style_cell={'width': '150',
                        'height': '60px',
                        'textAlign': 'left'})

        return table

    elif active_tab == "tab-2":
        shape = html.P(['Dataset Shape:', html.Br(), str(df.shape), html.Br(),
                        'Anzahal NaN Werte in Spalten:', html.Br(), str(df.isna().sum()), html.Br(),
                        ])
        return shape

    else:
        raise PreventUpdate


# take stored data, display column names and models in dropdown-menu
# TODO: Zwei gleiche Auswahlmögl. ausschließen
# TODO: JSON file as input
@app.callback(
    [Output('opt-dropdownX', 'options'),
     Output('opt-dropdownY', 'options'),
     Output("model", "options"),
     Output("model-cluster", "options")],
    [
        Input('upload', 'contents'),
        Input('upload', 'filename'),

    ]
)
def update_date_dropdown(contents, filename):
    optionsX = []
    optionsY = []
    model = [{'label': "Lineare Regression", 'value': "regression"},
             {'label': "Random Forest", 'value': "forest"}]
    model_cluster = [{"label": "K-Means", "value": "kmeans"}]
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)

        optionsX = [{'label': col, 'value': col} for col in df.columns]
        optionsY = [{'label': col, 'value': col} for col in df.columns]
    return optionsX, optionsY, model, model_cluster


# simple regression on input data and return figure
# TODO: JSON file as input
@app.callback(
    Output("regression-graph", "figure"),
    [Input('start-regression', 'n_clicks')],

    [State("opt-dropdownX", "value"),
     State("model", "value"),
     State('upload', 'contents'),
     State('upload', 'filename'),
     ],
)
def make_regression(n_clicks, y, model, contents, filename):
    if None in (contents, filename, y, model):
        raise PreventUpdate
    elif contents:
        contents = contents[0]
        filename = filename[0]
        contents = parse_data(contents, filename)

    if model == "regression":

        Y = contents[y]
        X = contents.drop(y, axis=1)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33)

        model = LinearRegression()
        model.fit(X_train, Y_train)

        Y_pred = model.predict(X_test)

        mse = sklearn.metrics.mean_squared_error(Y_test, Y_pred)
        print(mse)

        data = [
            go.Scatter(
                x=Y_test,
                y=Y_pred,
                mode="markers",
                marker={"size": 8},
            )

        ]

        layout = {"xaxis": {"title": "Actual " + y}, "yaxis": {"title": "Predicted " + y}}

    elif model == "forest":
        Y = contents[y]
        X = contents.drop(y, axis=1)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33)

        model = RandomForestClassifier(n_jobs=1, n_estimators=10)
        model.fit(X_train, Y_train)

        Y_pred = model.predict(X_test)

        data = [
            go.Scatter(
                x=Y_test,
                y=Y_pred,
                mode="markers",
                marker={"size": 8},
            )

        ]

        layout = {"xaxis": {"title": "Actual " + y}, "yaxis": {"title": "Predicted " + y}}


    elif model == None:
        print("Bitte Model auswählen")

    return go.Figure(data=data, layout=layout)


# simple clustering based on input data
# TODO: JSON file as input
@app.callback(
    Output("cluster-graph", "figure"),
    [Input('start-cluster', 'n_clicks')],

    [State("opt-dropdownX", "value"),
     State("opt-dropdownY", "value"),
     State("cluster-count", "value"),
     State('upload', 'contents'),
     State('upload', 'filename')
     ],
)
def make_clustering(n_clicks, x, y, n_clusters, contents, filename):
    if None in (contents, filename, x, y, n_clusters):
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
