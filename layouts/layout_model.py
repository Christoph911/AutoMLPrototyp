import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import nav
# define control panel for modelLayout

#TODO: Dropdown ins masterlayout?
controls_model = dbc.Card(
    [
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem('Supervised Learning',header=True),
                dbc.DropdownMenuItem('Lineare Regression',href='/model'),
                dbc.DropdownMenuItem('Unsupervised Learning',header=True),
                dbc.DropdownMenuItem('K-Means Clustering',href='/kmeans')
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



