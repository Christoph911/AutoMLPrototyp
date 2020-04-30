import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from main import app
from callbacks import callbacks_upload, callbacks_preprocessing,callbacks_linear_regression,callbacks_kmeans,callbacks_random_forest

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

choose_model = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem('Supervised Learning', header=True),
        dbc.DropdownMenuItem('Lineare Regression', href='/model'),
        dbc.DropdownMenuItem('Random Forest',href='/forest'),
        dbc.DropdownMenuItem('Unsupervised Learning', header=True),
        dbc.DropdownMenuItem('K-Means Clustering', href='/kmeans')
    ],
    label='Modellauswahl',
    bs_size='md',
),

# create layout for startpage
layout_start = dbc.Container(
    [
        html.H1("Automated Machine Learning Web-App - Willkommen!"),
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


