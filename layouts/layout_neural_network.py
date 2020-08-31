import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header

# define control panel for modelLayout

# TODO: Dropdown ins masterlayout?
controls_nn = dbc.Card(
    [
        html.H5("Auswahlmenü", style={'text-align': 'center'}),
        html.Hr(),
        dbc.FormGroup(
            [
                dbc.Label("Zielwert"),
                dcc.Dropdown(
                    id="zielwert-opt-nn",
                ),
                html.Div(id='zielwert-div'),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Optimizer"),
                dcc.Dropdown(
                    id="optimizer-nn",
                    options=[
                        {'label': 'Adam', 'value': 'adam'},
                        {'label': 'SGD', 'value': 'sgd'},
                    ],
                    value='adam'
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('Anzahl Epochen:'),
                dcc.Slider(
                    min=10,
                    max=100,
                    step=None,
                    marks={
                        10: '10', 20: '20', 30: '30',
                        40: '40', 50: '50', 60: '60',
                        70: '70', 80: '80', 90: '90', 100: '100'
                    },
                    value=10,
                    id='number-epochs'
                )
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('Train/Test-Size'),
                dcc.Slider(
                    min=0.3,
                    max=0.8,
                    step=None,
                    marks={
                        0.3: '30%/70%', 0.4: '40%/60%', 0.5: '50%/50%',
                        0.6: '60%/40', 0.7: '70%/30%', 0.8: '80%/20%',
                    },
                    value=0.7,
                    id='train-test-nn'
                )
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('Größe Validation Set:'),
                dcc.Slider(
                    min=0.1,
                    max=0.9,
                    step=None,
                    marks={
                        0.1: '10%', 0.2: '20%', 0.3: '30%',
                        0.4: '40%', 0.5: '50%', 0.6: '60%',
                        0.7: '70%', 0.8: '80%', 0.9: '90%'
                    },
                    value=0.1,
                    id='val-nn'
                )
            ]
        ),
        html.Hr(),
        dbc.FormGroup(
            [
                dbc.Button("Start!", color='success', id="start-nn-btn"),
            ]
        ),
    ],
    body=True
)

# define card for graph in modelLayout
card_graph_nn = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Vorschau", tab_id="tab-1-nn"),
                    dbc.Tab(label="Metriken", tab_id="tab-2-nn"),
                ],
                id="card-tabs-nn",
                card=True,
                active_tab="tab-1-nn",
            )
        ),
        dbc.CardBody(html.Div(id="tab-content-nn")),
    ]
)

layout_nn = dbc.Container(
    [
        html.Div(header),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_nn, md=4, align="start"),
                dbc.Col(card_graph_nn, md=8, align="start")

            ]
        ),
        html.Div(id='error-message-target-nn'),
        html.Div(id='error-message-model-nn')
    ],
    fluid=True,
)
