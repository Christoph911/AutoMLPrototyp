import base64
import io
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


from sklearn.cluster import KMeans


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
# TODO: Zwei gleiche Auswahlmögl. ausschließen
@app.callback(
    [Output('opt-dropdownX', 'options'),
     Output('opt-dropdownY', 'options'),
     Output("model","options")],
    [
        Input('upload', 'contents'),
        Input('upload', 'filename')

    ]
)
def update_date_dropdown(contents, filename):
    optionsX = []
    optionsY = []
    model = [{'label': "Lineare Regression", 'value': "regression"},
             {'label': "Random Forest", 'value': "forest"}]
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)

        optionsX = [{'label': col, 'value': col} for col in df.columns]
        optionsY = [{'label': col, 'value': col} for col in df.columns]
    return optionsX, optionsY, model


@app.callback(
    Output("regression-graph", "figure"),
    [Input('start-regression', 'n_clicks')],

    [State("opt-dropdownX", "value"),
     State("model","value"),
     State('upload', 'contents'),
     State('upload', 'filename')
     ],
)
def make_regression(n_clicks, x,model, contents, filename):
    layout = None
    data = []
    if contents is None or filename is None or x is None or model is None:
        raise PreventUpdate
    if model == "regression":
        if contents:
            contents = contents[0]
            filename = filename[0]
            contents = parse_data(contents, filename)

            Y = contents[x]
            X = contents.drop(x,axis=1)

            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33)

            model = LinearRegression()
            model.fit(X_train,Y_train)

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

            layout = {"xaxis": {"title": "Actual " + x}, "yaxis": {"title": "Predicted" + x}}

                #title=f"Score: {filename}, MSE: {mse:.3f} (Test Data)",
    elif model == "forest":
        print("Ich und mein Holz")

    elif model == None:
        print("Bitte Model auswählen")


    return go.Figure(data=data, layout=layout)

# output clustering
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