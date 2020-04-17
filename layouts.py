import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# define navbar
nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Supervised learning", href="/")),
        dbc.NavItem(dbc.NavLink("Unsupervised learning", href="/unsupervised")),
        dbc.NavItem(dbc.NavLink("Reinforcement learning", href='/')),
    ],
    pills=True,
)
# define controls for clustering operations
controls_clustering = dbc.Card(
    [

        dbc.FormGroup(
            [
                dcc.Upload(
                    id="upload",
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
                ),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("X-Achse"),
                dcc.Dropdown(
                    id="opt-dropdownX",
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
                    id="opt-dropdownY",
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
                dbc.Button("Let the magic happen!", id="start-cluster"),
            ]
        ),
    ],
    body=True,
)

controls_regression = dbc.Card(
    [
        dbc.FormGroup(
            [
                dcc.Upload(
                    id="upload",
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
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Zielwert"),
                dcc.Dropdown(
                    id="opt-dropdownX",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Button("Let the magic happen!", id="start-regression"),
            ]
        ),
    ],
    body=True

)

# make layouts
layout_supervised = dbc.Container(
    [
        html.H1("AutoML Prototyp"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_regression, md=4),
                dbc.Col(dcc.Graph(id="regression-graph"), md=8)
            ],
            align="center"
        )
    ],
    fluid=True,
)

layout_unsupervised = dbc.Container(
    [
        html.H1("AutoML Prototyp"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_clustering, md=4),
                # dbc.Col(html.Div(id="output-data-upload"), md=8)
                dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
            ],
            align="center",
        )
    ],
    fluid=True,
)
