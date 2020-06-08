import json
from main import app
from dash.dependencies import Input, Output, State
import pandas as pd

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
