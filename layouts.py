import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# define navbar
nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Unsupervised learning", active=True, href="/")),
        dbc.NavItem(dbc.NavLink("Supervised learning", href='/apps/app2')),
        dbc.NavItem(dbc.NavLink("Reinforcement learning", href='/')),
    ],
    pills=True,
)

controls_clustering = dbc.Card(
    [

        dbc.FormGroup(
            [
                dcc.Upload(
                    id="upload-data",
                    children=dbc.Button("Datensatz hochladen", color="secondary", outline=True, block=True),
                    multiple=True
                ),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("Modellauswahl"),
                dcc.Dropdown(
                    id="model",
                    options=[
                     {"label": "K-Means Clustering", "value": "k-means"}
                    ],
                ),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("X-Achse"),
                dcc.Dropdown(
                    id="x-variable",
                    # options=[
                    #   {"label": col, "value": col} for col in df.columns
                    # ],
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Y-Achse"),
                dcc.Dropdown(
                    id="y-variable",
                    # options=[
                    #    {"label": col, "value": col} for col in df.columns
                    # ],

                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Anzahl Cluster"),
                dbc.Input(id="cluster-count", type="number", value=3),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Button("Let the magic happen!",id="start"),
            ]
        ),
    ],
    body=True,
)

layout1 = dbc.Container(
    [
        html.H1("AutoML Prototyp"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_clustering, md=4),
                dbc.Col(html.Div(id="output-data-upload"), md=8)
                # dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
            ],
            align="center",
        )
    ],
    fluid=True,
)

layout2 = dbc.Container(
    [
        html.H1("AutoML Prototyp"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_clustering,md=4)
            ],
            align="center"
        )
    ],
    fluid=True,
)
