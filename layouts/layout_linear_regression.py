import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header, choose_model
# define control panel for modelLayout

#TODO: Dropdown ins masterlayout?
controls_linear_regression = dbc.Card(
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
                        id="zielwert-opt",
                    ),
                ]
            ),
            dbc.FormGroup(
                [
                    dbc.Label("Train/Test-Size"),
                    dcc.Dropdown(
                        id="train-test-opt",
                    ),
                ]
            ),
            dbc.FormGroup(
                [
                    dbc.Button("Let the magic happen!", id="start-regression-btn"),
                ]
            ),
        ],
        body=True
    )

# define card for graph in modelLayout
card_graph_linear_regression = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Vorschau", tab_id="tab-1-reg"),
                    dbc.Tab(label="Metriken", tab_id="tab-2-reg"),
                ],
                id="card-tabs-model",
                card=True,
                active_tab="tab-1-reg",
            )
        ),
        dbc.CardBody(html.Div(id='tab-content'))
    ]
)

layout_linear_regression = dbc.Container(
    [
        html.Div(header),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_linear_regression, md=4, align="start"),
                dbc.Col(card_graph_linear_regression, md=8, align="start")

            ]
        )
    ],
    fluid=True,
)



