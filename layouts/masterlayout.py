import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from main import app
from callbacks import callbacks_upload, callbacks_preprocessing,callbacks_model,callbacks_kmeans

# define navbar for mainLayout
nav = dbc.Nav(
    children=[
        dbc.NavItem(dbc.NavLink("1. Daten hochladen", href='/upload')),
        dbc.NavItem(dbc.NavLink("2. Preprocessing", href='/prep')),
        dbc.NavItem(dbc.NavLink("3. Modellauswahl", href='/model')),
        dbc.NavItem(dbc.NavLink("4. Evaluation", href='/eval')),
    ],
    pills=True,
)

# create layout for startpage
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



###METHOD NOT USED AT THE MOMENT###
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

###METHOD NOT USED AT THE MOMENT###
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

