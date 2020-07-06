import json
from main import app
import dash
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder

# get stored data, update dropdown, return selected target
@app.callback(
    [Output('input-column-1', 'options'),
    Output('input-column-2', 'options'),
     Output('drop-column-1', 'options'),
     Output('normalize-dropdown', 'options')],
    [Input('stored-data-upload', 'children'),
     Input('input-column-2-div', 'children')]
)
def get_target(df, dummy):
    print("Daten an Dropdown in prep Modul Übergeben")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    target_1 = [{'label': col, 'value': col} for col in df.columns]
    target_2 = [{'label': col, 'value': col} for col in df.columns]
    target_3 = [{'label': col, 'value': col} for col in df.columns]
    target_4 = [{'label': col, 'value': col} for col in df.columns]

    return target_1, target_2, target_3, target_4

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

@app.callback(
    [Output('table-prep', 'data'),
     Output('table-prep', 'columns')],
    [Input('add_column_btn', 'n_clicks'),
     Input('add_rows_btn', 'n_clicks'),
     Input('drop_rows_btn', 'n_clicks'),
     Input('add_column_math_btn','n_clicks'),
     Input('drop_column_btn', 'n_clicks'),
     Input('drop_null_btn', 'n_clicks'),
     Input('replace_null_btn', 'n_clicks'),
     Input('z_score_btn', 'n_clicks'),
     Input('min_max_scaler_btn', 'n_clicks'),
     Input('log_btn', 'n_clicks'),
     Input('label_encoding_btn', 'n_clicks'),
     Input('hot_encoding_btn', 'n_clicks')],
    [State('table-prep', 'data'),
     State('table-prep', 'columns'),
     State('add-column-name', 'value'),
     State('add-column-math-name','value'),
     State('add-column-value', 'value'),
     State('drop-column-1', 'value'),
     State('add-row-value', 'value'),
     State('row-count', 'value'),
     State('input-column-1', 'value'),
     State('operator','value'),
     State('input-column-2', 'value'),
     State('normalize-dropdown', 'value')
     ]
)
def update_table_prep(add_column_btn, add_rows_btn, drop_rows_btn, add_column_math_btn, drop_column_btn, drop_null_btn, replace_null_btn, z_score_btn, min_max_scaler_btn, log_btn, label_encoding_btn, hot_encoding_btn, rows, columns, column_name, column_math_name, column_value, col_1_drop, row_value, row_count, col_1, operator, col_2, normalize_dropdown):
    ctx = dash.callback_context
    #df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    table_data = pd.DataFrame.from_dict(rows)

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'add_column_btn':
            table_data[column_name] = column_value
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        elif button_id == 'add_rows_btn':
            rows.append({c['id']: row_value for c in columns})
            return rows, columns
        elif button_id == 'drop_rows_btn':
            table_data = table_data.drop([table_data.index[row_count]])
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        elif button_id == 'add_column_math_btn':
            if operator == '+':
                table_data[column_math_name] = table_data.loc[:, col_1] + table_data.loc[:, col_2]
            elif operator == '-':
                table_data[column_math_name] = table_data.loc[:, col_1] - table_data.loc[:, col_2]
            elif operator == '*':
                table_data[column_math_name] = table_data.loc[:, col_1] * table_data.loc[:, col_2]
            elif operator == '/':
                table_data[column_math_name] = table_data.loc[:, col_1] / table_data.loc[:, col_2]
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        elif button_id == 'drop_column_btn':
            if col_1_drop is not None:
                table_data = table_data.drop([col_1_drop], axis=1)
            elif col_1_drop is None:
                table_data = table_data.drop(table_data.columns, axis=1)
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        elif button_id == 'drop_null_btn':
            replace_values = {'': np.nan, 'Null': np.nan, 'null': np.nan, 'NaN': np.nan}
            table_data = table_data.replace(replace_values).dropna(axis=0)
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        elif button_id == 'replace_null_btn':
            replace_values = {'': np.nan, 'Null': np.nan, 'null': np.nan, 'NaN': np.nan}
            table_data = table_data.replace(replace_values)
            table_data = table_data.fillna(round(table_data.mean()))
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        elif button_id == 'z_score_btn':
            scaler = StandardScaler()
            scaled_values = scaler.fit_transform(table_data).round(5)
            scaled_values_df = pd.DataFrame(scaled_values, columns=[c['name'] for c in columns])
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return scaled_values_df.to_dict('records'), new_cols
        elif button_id == 'min_max_scaler_btn':
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_values = scaler.fit_transform(table_data).round(5)
            scaled_values_df = pd.DataFrame(scaled_values, columns=[c['name'] for c in columns])
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return scaled_values_df.to_dict('records'), new_cols
        elif button_id == 'log_btn':
            log_values = np.log(table_data).round(5)
            log_values_df = pd.DataFrame(log_values, columns=[c['name'] for c in columns])
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return log_values_df.to_dict('records'), new_cols
        elif button_id == 'label_encoding_btn':
            if normalize_dropdown is None:
                # get categorical values in dataframe
                categorical_values = table_data.select_dtypes(include=[object])
                # get numerical values in dataframe
                numerical_values = table_data.drop(categorical_values, axis=1)
                # create LabelEncoder Instance
                label_encoder = LabelEncoder()
                # encode categorical values
                encoded_values = categorical_values.apply(label_encoder.fit_transform)
                # join encoded and numerical values
                new_df = numerical_values.join(encoded_values)
            if normalize_dropdown is not None:
                choosen_column = table_data[normalize_dropdown]
                other_columns = table_data.drop([normalize_dropdown], axis=1)
                print(other_columns)
                label_encoder = LabelEncoder()
                encoded_values = label_encoder.fit_transform(choosen_column)
                print(encoded_values)

                dff = pd.DataFrame(encoded_values,columns=table_data[normalize_dropdown].columns)
                print(dff)
                new_df = pd.concat([other_columns,dff],axis=1)


            new_cols = [{"name": i, "id": i} for i in new_df.columns]
            return new_df.to_dict('records'), new_cols
        # elif button_id == 'hot_encoding_btn':
        #     # get categorical values in dataframe
        #     categorical_values = df.select_dtypes(include=[object])
        #     # get numerical values in dataframe
        #     numerical_values = df.drop(categorical_values, axis=1)
        #     # create LabelEncoder Instance
        #     label_encoder = LabelEncoder()
        #     # encode categorical values
        #     encoded_values = categorical_values.apply(label_encoder.fit_transform)
        #     # join encoded and numerical values
        #     oneHotencoder = OneHotEncoder()
        #     oneHotEncoded_values = oneHotencoder.fit_transform(encoded_values)
        #     print(oneHotEncoded_values)
        #
        #     new_df = numerical_values.join(oneHotEncoded_values)
        #     new_cols = [{"name": i, "id": i} for i in new_df.columns]
        #     return new_df.to_dict('records'), new_cols

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
