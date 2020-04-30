import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import nav

# define control panel for clustering operations
controls_clustering = dbc.Card(
    [
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem('Supervised Learning', header=True),
                dbc.DropdownMenuItem('Lineare Regression', href='/model'),
                dbc.DropdownMenuItem('Unsipervised Learning', header=True),
                dbc.DropdownMenuItem('K-Means Clustering', href='/unsupervised')
            ],
            label='Modellauswahl',
            bs_size='md',
        ),
        html.Hr(),
        dbc.FormGroup(
            [
                dbc.Button("Daten laden", id="load-data")
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("X-Achse"),
                dcc.Dropdown(
                    id="opt-dropdownX",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Y-Achse"),
                dcc.Dropdown(
                    id="opt-dropdownY",
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
layout_kmeans = dbc.Container(
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
        )
    ],
    fluid=True,
)
