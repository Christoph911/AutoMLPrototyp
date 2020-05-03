from main import app
from dash.dependencies import Input, Output

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