import json
from main import app
import dash
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
    [Input('add_column_btn', 'n_clicks'),
     Input('add_rows_btn', 'n_clicks'),
     Input('add_column_math_btn','n_clicks')],
    [State('table-prep', 'data'),
     State('table-prep', 'columns'),
     State('add-column-name', 'value'),
     State('add-column-value', 'value'),
     State('add-row-value', 'value'),
     State('input-column-1', 'value'),
     State('operator','value'),
     State('input-column-2', 'value')
     ]
)
def update_table_prep(add_column_btn, add_rows_btn,add_column_math_btn, rows, columns, column_name, column_value, row_value, col_1, operator, col_2):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'add_column_btn':
            df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
            table_data = df.from_dict(rows)
            table_data[column_name] = column_value
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        elif button_id == 'add_rows_btn':
            rows.append({c['id']: row_value for c in columns})
            return rows, columns
        elif button_id == 'add_column_math_btn':
            df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
            table_data = df.from_dict(rows)
            #table_data[column_name] = table_data.iloc[:, col_1] + eval(operator) + table_data.iloc[:, col_2]
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols

        # try:
        #     table_data['output-row'] = table_data.iloc[:,number_colum_1] operator table_data.iloc[:,number_column_2]
        # except:


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
