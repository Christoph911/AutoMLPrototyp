import json
from main import app
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
"""modul contains methods to update dataFrame and targetValue in specific models"""


###callbacks for all models###

@app.callback(
    Output('get-data-model', 'children'),
    [Input('stored-data-prep', 'children'),
     Input('stored-data-upload', 'children')]
)
def get_data(prepared_df, uploaded_df):
    if prepared_df is not None:
        return prepared_df
    else:
        return uploaded_df

error_message_get_target = dbc.Modal(
            [
                dbc.ModalHeader("Fehler!"),
                dbc.ModalBody(["Es konnte kein Datensatz für den Trainingsprozess gefunden werden:", html.Br(),
                               "Bitte stell sicher, dass ein Datensatz hochgeladen wurde!"]),
                dbc.ModalFooter("")
            ],
            is_open=True,
        )