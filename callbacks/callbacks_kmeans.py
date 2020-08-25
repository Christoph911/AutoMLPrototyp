import json
from main import app
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go
from sklearn.cluster import KMeans
import dash_bootstrap_components as dbc
from callbacks.callbacks_master import error_message_get_target

@app.callback(
    [Output('dropdownX-kmeans-opt', 'options'),
     Output('dropdownY-kmeans-opt', 'options'),
     Output('error-message-target-cluster', 'children')],
    [Input('get-data-model', 'children'),
     Input('zielwert-div', 'children')]
)
def update_dropdown(df, dummy):
    try:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

        optionsX = [{'label': col, 'value': col} for col in df.columns]
        optionsY = [{'label': col, 'value': col} for col in df.columns]

        return optionsX, optionsY, None
    except:
        error_message_get_target
        return None, None, error_message_get_target


# simple clustering based on input data
@app.callback(
    [Output('store-figure-kmeans', 'data'),
     Output('error-message-model-cluster', 'children')],
    [Input('start-cluster-btn', 'n_clicks')],
    [State('get-data-model', 'children'),
     State('dropdownX-kmeans-opt', 'value'),
     State('dropdownY-kmeans-opt', 'value'),
     State('cluster-count', 'value')]
)
def make_clustering(n_clicks, df, x, y, n_clusters):
    try:
        print("started clustering")
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

        km = KMeans(n_clusters=max(n_clusters, 1))
        df = df.loc[:, [x, y]]
        km.fit(df.values)
        df["cluster"] = km.labels_

        centers = km.cluster_centers_

        # build figure
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df.loc[df.cluster == c, x],
                    y=df.loc[df.cluster == c, y],
                    mode="markers",
                    marker={"size": 8},
                    name="Cluster {}".format(c)
                )
                for c in range(n_clusters)
            ]
        )

        fig.update_layout(
            xaxis_title=x,
            yaxis_title=y,
            template='plotly_white'
        )

        return dict(figure=fig), None
    except Exception as e:
        error_message_model = dbc.Modal(
            [
                dbc.ModalHeader("Fehler!"),
                dbc.ModalBody(["Es ist ein Fehler während des Trainingsprozesses aufgetreten:", html.Br(),
                               html.H6(str(e)), html.Br(),
                               " Bitte stell darüber hinaus sicher, dass der verwendete Datensatz keine Null-Values enthält "
                               "und das korrekte Modell für die Problemstellung ausgewählt wurde",html.Br(),
                               ]),
                dbc.ModalFooter("")
            ],
            is_open=True,
        )
        return None, error_message_model


# manage tab content
@app.callback(
    Output("tab-content-kmeans", "children"),
    [Input("card-tabs-kmeans", "active_tab"),
     Input("store-figure-kmeans", "data")],
)
def create_tab_content(active_tab, data):
    if active_tab and data is not None:
        if active_tab == "tab-1-kmeans":
            figure = dcc.Graph(figure=data["figure"])
            return figure
    return data
