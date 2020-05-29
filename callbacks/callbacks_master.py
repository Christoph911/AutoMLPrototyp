import json
from main import app
from dash.dependencies import Input, Output, State
import pandas as pd
"""modul contains methods to update dataFrame and targetValue in specific models"""

###callbacks for all models###

@app.callback(
    Output('get-data-model','children'),
    [Input('stored-data-prep','children'),
     Input('stored-data-upload','children')]
)
def get_data(new_df,stored_df):
    print("getData")
    if new_df is not None:
        return new_df
    else:
        return stored_df

# get stored data, update dropdown, return selected target
@app.callback(
    Output('zielwert-opt', 'options'),
    [Input('get-data-model', 'children'),
     Input('zielwert-div','children')]
)
def get_target(df,dummy):
    print("Daten an Dropdown Übergeben")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    target = [{'label': col, 'value': col} for col in df.columns]

    return target
