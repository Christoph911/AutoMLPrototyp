import json
from main import app

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objs as go

import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans

@app.callback(
    [Output('opt-dropdownX', 'options'),
     Output('opt-dropdownY', 'options'),
     Output("model", "options"),
     Output("model-cluster", "options"),
     Output('train-test','options')],
    [
        Input('stored-data', 'children'),
        Input("load-data", "n_clicks")

    ]
)
def update_date_dropdown(df, n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])
        model = [{'label': "Lineare Regression", 'value': "regression"},
                 {'label': "Random Forest", 'value': "forest"}]
        model_cluster = [{"label": "K-Means", "value": "kmeans"}]
        train_test_size = [{'label': '75% Train-size/25% Test-size','value': 0.25},
                           {'label': '60% Train-size/40% Test-size','value': 0.4}]

        optionsX = [{'label': col, 'value': col} for col in df.columns]
        optionsY = [{'label': col, 'value': col} for col in df.columns]

        return optionsX, optionsY, model, model_cluster,train_test_size
    else:
        raise PreventUpdate

#TODO: mse ausgeben lassen
# simple regression on input data and return figure
@app.callback(
    Output("regression-graph", "figure"),
    [Input('table-new', 'children'),
     Input("opt-dropdownX", "value"),
     Input("model", "value"),
     Input('train-test','value'),
     Input('card-tabs-model','active_tab'),
     Input('start-regression', 'n_clicks'),
     ],
)
def make_regression(df, y, model, train_test_size, active_tab, n_clicks):
    mse = None
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

    if active_tab == 'tab-1-model' and model == "regression":

        Y = df[y]
        X = df.drop(y, axis=1)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=train_test_size)

        model = LinearRegression()
        model.fit(X_train, Y_train)

        Y_pred = model.predict(X_test)

        mse = sklearn.metrics.mean_squared_error(Y_test, Y_pred)


        data = [
            go.Scatter(
                x=Y_test,
                y=Y_pred,
                mode="markers",
                marker={"size": 8},
            )

        ]

        layout = {"xaxis": {"title": "Actual " + y}, "yaxis": {"title": "Predicted " + y}}
        return go.Figure(data=data, layout=layout)

    elif active_tab == 'tab-1-model' and model == "forest":
        Y = df[y]
        X = df.drop(y, axis=1)

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

        return go.Figure(data=data, layout=layout)

    elif active_tab == "tab-2-model":
        raise PreventUpdate


    else:
        raise PreventUpdate


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