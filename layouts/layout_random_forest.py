import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import nav, choose_model

# define control panel for modelLayout

# TODO: Dropdown ins masterlayout?
controls_forest = dbc.Card(
    [
        html.Div(choose_model),
        html.Hr(),
        dbc.FormGroup(
            [
                dbc.Button("Daten laden", id="load-data")
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Zielwert"),
                dcc.Dropdown(
                    id="dropdownX-forest-opt",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Train/Test-Size"),
                dcc.Dropdown(
                    id="train-test-forest",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Button("Let the magic happen!", id="start-forest-btn"),
            ]
        ),
    ],
    body=True
)

# define card for graph in modelLayout
card_graph_forest = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label='Vorschau', tab_id='tab-1-forest'),
                    dbc.Tab(label='Metriken', tab_id='tab-2-forest'),
                ],
                id='card-tabs-forest',
                card=True,
                active_tab='tab-1-forest',
            )
        ),
        dbc.CardBody(dcc.Graph(id='forest-graph')),
    ]
)

layout_forest = dbc.Container(
    [
        html.H1('AutoML Prototyp - Modellauswahl'),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_forest, md=4, align='start'),
                dbc.Col(card_graph_forest, md=8, align='start')
            ]
        )
    ],
    fluid=True,
)
