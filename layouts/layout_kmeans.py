import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header

# define control panel for clustering operations
controls_clustering = dbc.Card(
    [
        html.H5("Auswahlmenü", style={'text-align': 'center'}),
        html.Hr(),
        dbc.FormGroup(
            [
                dbc.Label('X-Achse'),
                dcc.Dropdown(
                    id='dropdownX-kmeans-opt',
                ),
                html.Div(id='zielwert-div'),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('Y-Achse'),
                dcc.Dropdown(
                    id='dropdownY-kmeans-opt',
                ),
                html.Div(id='zielwert-div'),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('Anzahl Cluster'),
                dbc.Input(id='cluster-count', type='number', value=3),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Button('Start!', color='success', id='start-cluster-btn'),
            ]
        ),
    ],
    body=True,
)

card_graph_kmeans = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label='Vorschau', tab_id='tab-1-kmeans'),
                ],
                id='card-tabs-kmeans',
                card=True,
                active_tab='tab-1-kmeans',
            )
        ),
        dbc.CardBody(html.Div(id='tab-content-kmeans'))
    ]
)

layout_kmeans = dbc.Container(
    [
        html.Div(header),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_clustering, md=4, align='start'),
                dbc.Col(card_graph_kmeans, md=8, align='start'),
            ]
        )
    ],
    fluid=True,
)
