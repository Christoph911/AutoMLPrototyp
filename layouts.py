import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from main import app

# define navbar
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

),
# define control bar for upload layout
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

controls_prep = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Button("NaN-Values entfernen",id = "remove-NaN")
            ]
        )
    ]
)
# define controls for clustering operations
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
controls_model = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Button("Daten laden",id="load-data")
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
),
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
card_table_model = dbc.Card(
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


# make layouts
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
                        ['Schritt 1: Klicke auf den Button "1. Daten hochladen" in der Kopfzeile und folge den Anweisungen', html.Br(),
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
                dbc.Col(controls_upload, md=4,align="start"),
                #dbc.Col(html.Div(id="table-head"), md=8)
                dbc.Col(card_table_upload,md=8,align="start")
                #dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
            ],

        )
    ],
    fluid=True,
),

layout_prep = dbc.Container(
    [
        html.H1("AutoML Prototyp - Preprocessing"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_prep,md=4,align="start"),
                dbc.Col(html.Div(id="data-prepared"),md=4,align="start")

            ]
        )
    ],
    fluid=True,
),
layout_model = dbc.Container(
    [
        html.H1("AutoML Prototyp - Modellauswahl"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_model,md=4,align="start"),
                dbc.Col(card_table_model,md=8,align="start")
                #dbc.Col(dcc.Graph(id='regression-graph'),md=8),
                #dbc.Col(html.Div(id="data-prepared"),md=4,align="start")

            ]
        )
    ],
    fluid=True,
),
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
