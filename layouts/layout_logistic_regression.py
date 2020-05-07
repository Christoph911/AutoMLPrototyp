import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header, choose_model
# define control panel for modelLayout

#TODO: Dropdown ins masterlayout?
controls_logistic_regression = dbc.Card(
        [
            dbc.FormGroup(
                [
                    dbc.Button("Daten laden", id="load-data")
                ]
            ),
            dbc.FormGroup(
                [
                    dbc.Label("Zielwert"),
                    dcc.Dropdown(
                        id="zielwert-opt-log",
                    ),
                ]
            ),
            dbc.FormGroup(
                [
                    dbc.Label("Train/Test-Size"),
                    dcc.Dropdown(
                        id="train-test-opt-log",
                    ),
                ]
            ),
            dbc.FormGroup(
                [
                    dbc.Button("Let the magic happen!", id="start-logistic-regression-btn"),
                ]
            ),
        ],
        body=True
    )

# define card for graph in modelLayout
card_graph_logistic_regression = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Vorschau", tab_id="tab-1-log-reg"),
                    dbc.Tab(label="Metriken", tab_id="tab-2-log-reg"),
                ],
                id="card-tabs-logistic-reg",
                card=True,
                active_tab="tab-1-log-reg",
            )
        ),
        dbc.CardBody(dcc.Graph(id="logistic-regression-graph")),
    ]
)

layout_logistic_regression = dbc.Container(
    [
        html.Div(header),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_logistic_regression, md=4, align="start"),
                dbc.Col(card_graph_logistic_regression, md=8, align="start")

            ]
        )
    ],
    fluid=True,
)



