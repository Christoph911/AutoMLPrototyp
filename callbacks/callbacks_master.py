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
    [Input('load-data', 'n_clicks')],
    [State('get-data-model', 'children')]
)

###callbacks for supervised models###
def get_target(n_clicks, df):
    print("Daten an Dropdown Übergeben")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    target = [{'label': col, 'value': col} for col in df.columns]

    return target

# get slider value, return train size
@app.callback(
    Output('train-test','value')
)
def get_train_test_size(slider):
    train_test_size = [{'marks':marks} for marks in slider]
    return train_test_size