import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from main import app

# define navbar for mainLayout
nav = dbc.Nav(
    children=[
        dbc.NavItem(dbc.NavLink("1. Daten hochladen", href='/upload')),
        dbc.NavItem(dbc.NavLink("2. Preprocessing", href='/prep')),
        dbc.NavItem(dbc.NavLink("3. Modelauswahl", href='/model')),
        dbc.NavItem(dbc.NavLink("4. Evaluation", href='/eval')),
        dbc.NavItem(dbc.NavLink("TEST_Supervised learning", href="/supervised")),
        dbc.NavItem(dbc.NavLink("TEST_Unsupervised learning", href="/unsupervised")),

    ],
    pills=True,

)

# define control panel for uploadLayout
controls_upload = dbc.Card(
    [
        dbc.FormGroup(
            [
                dcc.Upload(
                    id="upload",
                    children=dbc.Button("Datensatz hochladen", color="secondary", outline=True, block=True),
                    multiple=True
                ),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Button("Zeige Vorschau an", id="start-preprocessing"),
            ]
        ),
    ]
)
# define control panel for prepLayout
controls_prep = dbc.Card(
    [
        dbc.FormGroup(
            [dbc.Button('Daten laden', id='load-table'),
             html.Br(),
             dbc.Button("NaN-Values entfernen", id="remove-NaN"),
             html.Br(),
             dbc.Button('Änderungen speichern', id='save-table-changes-btn')
             ]
        )
    ]
)
# define control panel for clustering operations
controls_clustering = dbc.Card(
    [

        dbc.FormGroup(
            [
                dcc.Upload(
                    id="upload",
                    children=dbc.Button("Datensatz hochladen", color="secondary", outline=True, block=True),
                    multiple=True
                ),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("Modellauswahl"),
                dcc.Dropdown(
                    id="model-cluster",
                ),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("X-Achse"),
                dcc.Dropdown(
                    id="opt-dropdownX",
                    # options=[
                    #   {"label": col, "value": col} for col in df.columns
                    # ],
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Y-Achse"),
                dcc.Dropdown(
                    id="opt-dropdownY",
                    # options=[
                    #    {"label": col, "value": col} for col in df.columns
                    # ],

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
# define control panel for regression operations
controls_regression = dbc.Card(
    [
        dbc.FormGroup(
            [
                dcc.Upload(
                    id="upload",
                    children=dbc.Button("Datensatz hochladen", color="secondary", outline=True, block=True),
                    multiple=True
                ),
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
                dbc.Button("Let the magic happen!", id="start-regression"),
            ]
        ),
    ],
    body=True

)
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
# define card for table and metrics in uploadLayout
card_table_upload = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Vorschau", tab_id="tab-1"),
                    dbc.Tab(label="Infos", tab_id="tab-2"),
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(html.Div(id="table-head")),
    ]
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
# define card for table in prepLayout
card_table_prep = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Vorschau", tab_id="tab-1-prep"),
                ],
                id="card-tabs-prep",
                card=True,
                active_tab="tab-1-prep",
            )
        ),
        dbc.CardBody(
            html.Div([
                dcc.Input(
                    id='add-column-name',
                    placeholder='Spaltennaamme eingeben',
                    value='',
                    style={'paadding': 10}
                ),
                html.Button('Spalte hinzufügen', id='add-column-button', style={'margin': 10}),
                html.Div(id="table-prep"),
                html.Button('Reihe hinzufügen', id='add-rows-button')

            ]),

        ),
    ]
)


# create layout pages
layout_start = dbc.Container(
    [
        html.H1("AutoML Prototyp - Willkommen!"),
        html.Div(nav),
        html.Hr(),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Herzlich Willkommen!", className="card-title"),
                    html.P(
                        "Willkommen bei der AutoML Webapp!"),
                    html.P(
                        "Bitte gehe nach folgenden Schritten vor:"),
                    html.P(
                        [
                            'Schritt 1: Klicke auf den Button "1. Daten hochladen" in der Kopfzeile und folge den Anweisungen',
                            html.Br(),
                            'Schritt 2: ', html.Br(),
                            'Schritt 3: ', html.Br(),
                            'Schritt 4: ', html.Br(),
                            'Schritt 5: ', html.Br(),
                            ''

                            ]
                    )
                ]
            )
        )
    ]

)

layout_upload = dbc.Container(
    [
        html.H1("AutoML Prototyp - Daten hochladen"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_upload, md=4, align="start"),
                dbc.Col(card_table_upload, md=8, align="start")
            ],

        )
    ],
    fluid=True,
)

layout_prep = dbc.Container(
    [
        html.H1("AutoML Prototyp - Preprocessing"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_prep, md=4, align="start"),
                dbc.Col(card_table_prep, md=8, align='start'),
                dbc.Col(html.Div(id="data-prepared"), md=4, align="start")

            ]
        )
    ],
    fluid=True,
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

layout_supervised = dbc.Container(
    [
        html.H1("AutoML Prototyp - Supervised Learning"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_regression, md=4),
                dbc.Col(dcc.Graph(id="regression-graph"), md=8)
            ],
            align="center"
        )
    ],
    fluid=True,
)

layout_unsupervised = dbc.Container(
    [
        html.H1("AutoML Prototyp"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_clustering, md=4),
                # dbc.Col(html.Div(id="output-data-upload"), md=8)
                dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
            ],
            align="center",
        )
    ],
    fluid=True,
)
