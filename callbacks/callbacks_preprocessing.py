import json
from main import app
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np


@app.callback(
    Output('table-prep', 'children'),
    [Input('stored-data-upload', 'children')]
)
def display_table_prep(df):
    if df is None:
        raise PreventUpdate

    elif df is not None:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

        table = dash_table.DataTable(
            id='table-prep',
            columns=[{"name": i, "id": i, 'deletable': True, 'renamable': True} for i in df.columns],
            data=df.to_dict("rows"),
            style_cell={'width': '150',
                        'height': '60px',
                        'textAlign': 'left'},

            editable=True,
            row_deletable=True,
            page_action='none',
            style_table={'height': '600px', 'overflowY': 'auto'}
        )
        return table

#
#
# @app.callback(
#     Output('table-prep', 'columns'),
#     [Input('add-column-btn', 'n_clicks')],
#     [State('add-column-name', 'value'),
#      State('table-prep', 'columns')])
# def update_table_prep_columns(n_clicks, value, existing_columns):
#     if n_clicks is None:
#         raise PreventUpdate
#     elif n_clicks is not None:
#         existing_columns.append({
#             'id': value, 'name': value,
#             'renamable': True, 'deletable': True
#         })
#     return existing_columns


# @app.callback(
#     Output('table-prep', 'data')
#     [Input('remove-null-btn', 'n_clicks')],
#     [State('table-prep', 'data'),
#      State('table-prep', 'columns')]
# )
# def drop_null_values(n_clicks, rows, columns):
#     if rows == '':
#         rows = ({c['id']: 'NULL' for c in columns})
#
#
#     return rows

@app.callback(
    [Output('table-prep', 'data'),
     Output('table-prep', 'columns')],
    [Input('add-column-btn', 'n_clicks')],
    [State('table-prep', 'data'),
     State('table-prep', 'columns'),
     State('add-column-name', 'value'),
     State('add-column-value', 'value')
     ]
)
def update_columns(n_clicks, rows, columns,column_name, column_value):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    table_data = df.from_dict(rows)
    try:
        table_data['output-row'] = table_data['Installed Capacity (MW)'] * table_data['Generation (GWh)']
    except:
        table_data[column_name] = column_value

    new_cols = [{"name": i, "id": i} for i in table_data.columns]
    return table_data.to_dict('records'), new_cols


@app.callback(
    Output('table-prep-row', 'data'),
    [Input('add-rows-btn', 'n_clicks')],
    [State('table-prep', 'data'),
     State('table-prep', 'columns'),
     State('add-row-value', 'value'),]
)
def update_table_prep_rows(n_clicks, rows,columns,value):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        rows.append({c['id']: value for c in columns})
        return rows


@app.callback(
    Output('stored-data-prep', 'children'),
    [Input('save-table-changes-btn', 'n_clicks')],
    [State('table-prep', 'data'),
     State('table-prep', 'columns')]
)
def save_data_prep(n_clicks, rows, columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    df = df.replace('', np.nan).dropna()
    df = df.to_json(orient='split')
    print("Geänderte Table in Div gespeichert und Null Values entfernt")
    return df
