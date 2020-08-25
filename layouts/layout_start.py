import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header
from main import app
from dash.dependencies import Input, Output, State

# create modal element for information
info_modal = dbc.Modal(
    [
        dbc.ModalHeader("Changelog: 13.08.2020"),
        dbc.ModalBody(["- Einlesen von Excel-Dateien ermöglicht", html.Br(),
                      "- Div. Fehler in der Datenbearbeitung behoben", html.Br(),
                       "- Begonnen Fehler abzufangen"]),
        dbc.ModalFooter("")
     ],
     is_open=True,
)
# create layout for startpage
layout_start = dbc.Container(
    [  # TODO: place css in own file and make img size responsive
        html.Div(header),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Herzlich Willkommen!", className="card-title"),
                    html.P(
                        "Willkommen bei der Automated Machine Learning Web-App!"),
                    html.P(
                        "Zur Analyse eines Datensatzes gehen Sie bitte nach folgenden Schritten vor:"),
                    html.P(
                        [
                            '1: Klicken Sie auf den Button "Beginnen" oder "1. Datensatz hochladen" in der Kopfleiste, um mit dem Programm zu starten.',
                            html.Br(),
                            '2: Klicken Sie in der folgenden Ansicht auf "Datensatz hochladen", um einen Datensatz von der Festplatte in das Programm einzulesen.', html.Br(),
                            '3: Klicken Sie in der Kopfleiste auf "2. Datensatz bearbeiten", sofern Sie den Datensatz verändern möchten.', html.Br(),
                            '4: Klicken Sie in der Kopfleiste auf "3. Modellauswahl", um das Modell zur Berechnung auszuwählen und wählen Sie das gewünschte Modell.', html.Br(),
                            '5: Wählen Sie innerhalb des Modelles den Zielwert des Datensatzes sowie die angezeigten Einstellungsparameter aus.', html.Br(),
                            '6: Klicken Sie auf den Button "Starten", um das Modelltraining zu starten.', html.Br(),
                            '7: Folgend werden auf der rechten Karte die Modellergebnisse angezeigt.', html.Br(),
                            '8: Sie haben die Möglichkeit, über die Tabs der Karte weitere Modellergebnisse anzeigen zu lassen.', html.Br(),


                        ]
                    ),
                    dbc.Button('Beginnen', color='success', size='lg', href='/upload', style={'float': 'right'})
                ]
            ),
        ),
        # place modal element on start_layout
        info_modal
    ],
    fluid=True

)