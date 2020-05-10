import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header
# define control panel for modelLayout

#TODO: Dropdown ins masterlayout?
controls_nn = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Button("Daten laden", id="load-data-nn")
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Zielwert"),
                dcc.Dropdown(
                    id="zielwert-opt-nn",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Button("Let the magic happen!", id="start-nn-btn"),
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
        )
    ],
    fluid=True,
)



