import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header, choose_model

# define control panel for clustering operations
controls_clustering = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Button('Daten laden', id='load-data-btn')
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label('X-Achse'),
                dcc.Dropdown(
                    id='dropdownX-kmeans-opt',
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('Y-Achse'),
                dcc.Dropdown(
                    id='dropdownY-kmeans-opt',
                ),
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
                dbc.Button('Let the magic happen!', id='start-cluster-btn'),
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
                    dbc.Tab(label='Metriken', tab_id='tab-2-kmeans')
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
