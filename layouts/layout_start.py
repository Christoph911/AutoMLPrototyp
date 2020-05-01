import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header

# create layout for startpage
layout_start = dbc.Container(
    [   #TODO: place css in own file and make img size responsive
        html.Div(header),
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
    ],
    fluid=True

)


