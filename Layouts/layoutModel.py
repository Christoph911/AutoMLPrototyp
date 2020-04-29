import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Layouts.masterlayout import nav
from main import app
from Callbacks import callbacksModel

# define control panel for modelLayout
controls_model = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Button("Daten laden", id="load-data")
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
                dbc.Label("Train/Test-Size"),
                dcc.Dropdown(
                    id="train-test",
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

# define card for graph in modelLayout
card_graph_model = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Vorschau", tab_id="tab-1-model"),
                    dbc.Tab(label="Metriken", tab_id="tab-2-model"),
                ],
                id="card-tabs-model",
                card=True,
                active_tab="tab-1-model",
            )
        ),
        dbc.CardBody(dcc.Graph(id="regression-graph")),
    ]
)

layout_model = dbc.Container(
    [
        html.H1("AutoML Prototyp - Modellauswahl"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_model, md=4, align="start"),
                dbc.Col(card_graph_model, md=8, align="start")
                # dbc.Col(dcc.Graph(id='regression-graph'),md=8),
                # dbc.Col(html.Div(id="data-prepared"),md=4,align="start")

            ]
        )
    ],
    fluid=True,
)
