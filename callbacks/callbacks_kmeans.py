import json
from main import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
from sklearn.cluster import KMeans


@app.callback(
    [Output('dropdownX-kmeans-opt', 'options'),
     Output('dropdownY-kmeans-opt', 'options')],
    [
        Input('table-new', 'children'),
        Input('load-data-btn', 'n_clicks')

    ]
)
def update_date_dropdown(df, n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

        optionsX = [{'label': col, 'value': col} for col in df.columns]
        optionsY = [{'label': col, 'value': col} for col in df.columns]

        return optionsX, optionsY
    else:
        raise PreventUpdate


# simple clustering based on input data
# TODO: JSON file as input
@app.callback(
    Output('cluster-graph', 'figure'),
    [Input('table-new', 'children'),
     Input('dropdownX-kmeans-opt', 'value'),
     Input('dropdownY-kmeans-opt', 'value'),
     Input('cluster-count', 'value'),
     Input('start-cluster-btn', 'n_clicks'),
     ],
)
def make_clustering(df, x, y, n_clusters, n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        print("started clustering")
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

        km = KMeans(n_clusters=max(n_clusters, 1))
        df = df.loc[:, [x, y]]
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
                marker={"color": "#000", "size": 12, "symbol": "diamond",'template':'plotly_white'},
                name="Cluster centers",
            )
        )

        layout = {"xaxis": {"title": x}, "yaxis": {"title": y}}

        return go.Figure(data=data, layout=layout)
