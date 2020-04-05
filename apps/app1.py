###IMPORTS###
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from sklearn import datasets
from sklearn.cluster import KMeans
from main import app

###SETUP###
iris_raw = datasets.load_iris()
iris = pd.DataFrame(iris_raw["data"], columns=iris_raw["feature_names"])
boston_raw = datasets.load_boston()
boston = pd.DataFrame(boston_raw["data"],columns=boston_raw["feature_names"])

###LAYOUT###

# make Card including dropdown menu
controls_clustering = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Datensatz"),
                dcc.Dropdown(
                    id="datensatz",
                    options=[
                        {"label": "Iris", "value": "iris"},
                        {"label": "Boston", "value": "boston"}
                    ],
                    value="name",
                ),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[
                        {"label": col, "value": col} for col in iris.columns
                    ],
                    value="sepal length (cm)",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[
                        {"label": col, "value": col} for col in iris.columns
                    ],
                    value="sepal width (cm)",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Cluster count"),
                dbc.Input(id="cluster-count", type="number", value=3),
            ]
        ),
    ],
    body=True,
)

# define dropdown for regression
controls_regression = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Test"),
                dcc.Dropdown(
                    id="test",
                    options=[
                        {"label": "1", "value": "col"}
                    ],
                    value="test",
                ),
            ]
        )
    ]
)

# define navbar to change page
nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Clustering", active=True, href="/")),
        dbc.NavItem(dbc.NavLink("Regression", href='/apps/app2')),
    ],
    pills=True,
)

# create masterlayout
layout = dbc.Container(
    [
        html.H1("AutoML Prototyp"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_clustering, md=4),
                dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

# callback and method for datensatz dropdown
@app.callback(
    Output("datensatz", "children"),
    [
        Input("datensatz", "value"),
    ],
)
def choose_dataset(name):
    data = None
    if name == "iris":
        data = datasets.load_iris()
    elif name == "boston":
        data = datasets.load_boston()
    return print(data)


# callbacks for other dropdowns
@app.callback(
    Output("cluster-graph", "figure"),
    [
        Input("x-variable", "value"),
        Input("y-variable", "value"),
        Input("cluster-count", "value"),
    ],
)
###VISUALS###
def make_graph(x, y, n_clusters):
    # minimal input validation, make sure there's at least one cluster
    km = KMeans(n_clusters=max(n_clusters, 1))
    df = iris.loc[:, [x, y]]
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


# make sure that x and y values can't be the same variable in dropdown
def filter_options(v):
    """Disable option v"""
    return [
        {"label": col, "value": col, "disabled": col == v}
        for col in iris.columns
    ]


# functionality is the same for both dropdowns, so we reuse filter_options
app.callback(Output("x-variable", "options"), [Input("y-variable", "value")])(
    filter_options
)
app.callback(Output("y-variable", "options"), [Input("x-variable", "value")])(
    filter_options
)
