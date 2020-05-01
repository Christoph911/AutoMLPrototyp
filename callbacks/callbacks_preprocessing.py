import json
from main import app
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np


@app.callback(
    Output('table-prep', 'children'),
    [Input('stored-data', 'children')]
)
def display_table_prep(df):
    if df == None:
        raise PreventUpdate

    elif df != None:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

        table = dash_table.DataTable(
            id='table-prep',
            columns=[{"name": i, "id": i, 'deletable': True, 'renamable': True} for i in df.columns],
            data=df.to_dict("rows"),
            style_cell={'width': '150',
                        'height': '60px',
                        'textAlign': 'left'},

                    editable = True,
                    row_deletable = True,
        )
        return table

@app.callback(
    Output('table-prep', 'data'),
    [Input('add-rows-btn', 'n_clicks')],
    [State('table-prep', 'data'),
     State('table-prep', 'columns')]
)
def update_table_prep_rows(n_clicks,rows,columns):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        rows.append({c['id']: '' for c in columns})
        return rows

@app.callback(
    Output('table-prep', 'columns'),
    [Input('add-column-btn', 'n_clicks')],
    [State('add-column-name', 'value'),
     State('table-prep', 'columns')])
def update_table_prep_columns(n_clicks, value, existing_columns):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        existing_columns.append({
            'id': value, 'name': value,
            'renamable': True, 'deletable': True
        })
    return existing_columns


@app.callback(
    Output('table-new', 'children'),
    [Input('save-table-changes-btn', 'n_clicks')],
    [State('table-prep', 'data'),
     State('table-prep', 'columns')]
)
def save_table_prep_changes(n_clicks, rows, columns):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        # TODO: Konvertierung direkt in JSON möglich?
        df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
        df = df.replace('', np.nan)
        df = df.dropna()
        df = df.to_json(orient='split')
        print("Geänderte Table in Div gespeichert und Null Values entfernt")
        return df
