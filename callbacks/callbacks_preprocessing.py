import json
import sys
from main import app
import dash
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder

# get stored data, update dropdown, return selected target
@app.callback(
    [Output('input-column-1', 'options'),
     Output('input-column-2', 'options'),
     Output('drop-column-1', 'options'),
     Output('normalize-dropdown', 'options'),
     Output('dropNull-dropdown', 'options'),
     Output('drop-column-expression-drp', 'options'),
     Output('create-column-math', 'options')],
    [Input('stored-data-upload', 'children'),
     Input('input-column-2-div', 'children')]
)
def get_target(df, dummy):
    print("Daten an Dropdown in prep Modul Übergeben")
    if df is None:
        raise PreventUpdate
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    target_1 = [{'label': col, 'value': col} for col in df.columns]
    target_2 = [{'label': col, 'value': col} for col in df.columns]
    target_3 = [{'label': col, 'value': col} for col in df.columns]
    target_4 = [{'label': col, 'value': col} for col in df.columns]
    target_5 = [{'label': col, 'value': col} for col in df.columns]
    target_6 = [{'label': col, 'value': col} for col in df.columns]
    target_7 = [{'label': col, 'value': col} for col in df.columns]

    return target_1, target_2, target_3, target_4, target_5, target_6, target_7


# create Dash DataTable
@app.callback(
    Output('table-prep', 'children'),
    [Input('stored-data-upload', 'children')]
)
def create_table_prep(df):
    if df is None:
        raise PreventUpdate
    elif df is not None:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns']).convert_dtypes()
        table = dash_table.DataTable(
            id='table-prep',
            columns=[{"name": i, "id": i, 'deletable': True, 'renamable': True} for i in df.columns],
            data=df.to_dict("rows"),
            style_data={
                'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            fixed_rows={'headers': True, 'data': 0},
            editable=True,
            row_deletable=True,
            sort_action='native',
            filter_action="native",  # clientside filtering
            sort_mode="multi",
            column_selectable="single",
            selected_columns=[],
            page_action="native",
            page_current=0,
            page_size=50,
            virtualization=True,
        )
        return table


# get user input and update table
@app.callback(
    [Output('table-prep', 'data'),
     Output('table-prep', 'columns')],
    [Input('add_column_btn', 'n_clicks'),
     Input('add_rows_btn', 'n_clicks'),
     Input('drop_rows_btn', 'n_clicks'),
     Input('add_column_math_btn', 'n_clicks'),
     Input('drop_column_btn', 'n_clicks'),
     Input('drop_null_btn', 'n_clicks'),
     Input('replace_null_btn', 'n_clicks'),
     Input('z_score_btn', 'n_clicks'),
     Input('min_max_scaler_btn', 'n_clicks'),
     Input('log_btn', 'n_clicks'),
     Input('label_encoding_btn', 'n_clicks'),
     Input('drop_column_expr_btn', 'n_clicks'),
     Input('create_column_math_btn', 'n_clicks')],
    [State('table-prep', 'data'),
     State('table-prep', 'columns'),
     State('add-column-name', 'value'),
     State('add-column-math-name', 'value'),
     State('add-column-value', 'value'),
     State('drop-column-1', 'value'),
     State('add-column-math-name-2', 'value'),
     State('create-column-math','value'),
     State('operator-create-column', 'value'),
     State('input-math', 'value'),
     State('add-row-value', 'value'),
     State('row-count', 'value'),
     State('input-column-1', 'value'),
     State('operator', 'value'),
     State('input-column-2', 'value'),
     State('normalize-dropdown', 'value'),
     State('dropNull-dropdown', 'value'),
     State('user-input', 'value'),
     State('column-expression', 'value'),
     State('drop-column-expression-drp', 'value')
     ]
)
def update_table_prep(add_column_btn, add_rows_btn, drop_rows_btn, add_column_math_btn, drop_column_btn, drop_null_btn,
                      replace_null_btn, z_score_btn, min_max_scaler_btn, log_btn, label_encoding_btn,
                      drop_column_expr_btn,create_column_math_btn, rows, columns, column_name, column_math_name, column_value, col_1_drop,
                      add_column_math_name_2, create_column_math, operator_create_column, input_math, row_value, row_count, col_1, operator, col_2, normalize_dropdown, drop_null_dropdown, user_input,
                      column_expression, drop_column_expression_drp):
    # create callback context to get different button id´s
    ctx = dash.callback_context
    # create dataFrame out of data in Dash DataTable
    table_data = pd.DataFrame.from_dict(rows)
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        ### column operations ###
        # create new column and fill with input values
        if button_id == 'add_column_btn':
            table_data[column_name] = column_value
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        # create new column on two existing columns
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
        # create new column with math operation
        elif button_id == 'create_column_math_btn':
            if operator_create_column == '+':
                table_data[add_column_math_name_2] = table_data.loc[:, create_column_math] + input_math
            elif operator_create_column == '-':
                table_data[add_column_math_name_2] = table_data.loc[:, create_column_math] - input_math
            elif operator_create_column == '*':
                table_data[add_column_math_name_2] = table_data.loc[:, create_column_math] * input_math
            elif operator_create_column == '/':
                table_data[add_column_math_name_2] = table_data.loc[:, create_column_math] / input_math
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        # drop all selected columns
        elif button_id == 'drop_column_btn':
            if col_1_drop is not None:
                for x in col_1_drop:
                    table_data = table_data.drop([x], axis=1)
            elif col_1_drop is None:
                raise PreventUpdate
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        # drop values based on condition in column
        elif button_id == 'drop_column_expr_btn':
            if drop_column_expression_drp is not None:
                if column_expression == '>':
                    table_data = table_data.drop(table_data[table_data[col_1_drop] > user_input].index)
                elif column_expression == '>=':
                    table_data = table_data.drop(table_data[table_data[col_1_drop] >= user_input].index)
                elif column_expression == '<':
                    table_data = table_data.drop(table_data[table_data[col_1_drop] < user_input].index)
                elif column_expression == '<=':
                    table_data = table_data.drop(table_data[table_data[col_1_drop] <= user_input].index)
                elif column_expression == '=':
                    table_data = table_data.drop(table_data[table_data[col_1_drop] == user_input].index)
            elif drop_column_expression_drp is None:
                raise PreventUpdate
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        ### row operations ###
        # append new row with values
        elif button_id == 'add_rows_btn':
            rows.append({c['id']: row_value for c in columns})
            return rows, columns
        # drop row
        elif button_id == 'drop_rows_btn':
            table_data = table_data.drop([table_data.index[row_count]])
            return table_data.to_dict('records'), columns
        ### null operations ###
        # drop rows with null values in column or whole dataFrame
        elif button_id == 'drop_null_btn':
            replace_values = {'': np.nan, 'Null': np.nan, 'null': np.nan, 'NaN': np.nan}
            if drop_null_dropdown is None:
                table_data = table_data.replace(replace_values).dropna(axis=0)
            if drop_null_dropdown is not None:
                for x in drop_null_dropdown:
                    table_data = table_data.replace(replace_values).dropna(subset=[x], axis=0)
            return table_data.to_dict('records'), columns
        # replace rows with null values with column mean
        elif button_id == 'replace_null_btn':
            replace_values = {'': np.nan, 'Null': np.nan, 'null': np.nan, 'NaN': np.nan}
            table_data = table_data.replace(replace_values)
            table_data = table_data.fillna(round(table_data.mean()))
            return table_data.to_dict('records'), columns
        ### normalize operations ###
        # z-score
        elif button_id == 'z_score_btn':
            standard_scaler = StandardScaler()
            if normalize_dropdown is None:
                table_data = standard_scaler.fit_transform(table_data).round(5)
                table_data = pd.DataFrame(table_data, columns=[c['name'] for c in columns])
            elif normalize_dropdown is not None:
                for x in normalize_dropdown:
                    table_data[[x]] = standard_scaler.fit_transform(table_data[[x]]).round(5)
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        # minMax scaler
        elif button_id == 'min_max_scaler_btn':
            min_max_scaler = MinMaxScaler(feature_range=(0, 1))
            if normalize_dropdown is None:
                table_data = min_max_scaler.fit_transform(table_data).round(5)
                table_data = pd.DataFrame(table_data, columns=[c['name'] for c in columns])
            elif normalize_dropdown is not None:
                for x in normalize_dropdown:
                    table_data[[x]] = min_max_scaler.fit_transform(table_data[[x]]).round(5)
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        # log
        elif button_id == 'log_btn':
            if normalize_dropdown is None:
                table_data = np.log(table_data).round(5)
                table_data = pd.DataFrame(table_data, columns=[c['name'] for c in columns])
            if normalize_dropdown is not None:
                for x in normalize_dropdown:
                    table_data[[x]] = np.log(table_data[[x]].values.reshape(-1, 1)).round(5)
            new_cols = [{"name": i, "id": i} for i in table_data.columns]
            return table_data.to_dict('records'), new_cols
        elif button_id == 'label_encoding_btn':
            # create LabelEncoder Instance
            label_encoder = LabelEncoder()
            if normalize_dropdown is None:
                # get categorical values in dataframe
                categorical_values = table_data.select_dtypes(include=[object])
                # get numerical values in dataframe
                numerical_values = table_data.drop(categorical_values, axis=1)
                # encode categorical values
                encoded_values = categorical_values.apply(label_encoder.fit_transform)
                # join encoded and numerical values
                new_df = numerical_values.join(encoded_values)
            if normalize_dropdown is not None:
                raise PreventUpdate
            new_cols = [{"name": i, "id": i} for i in new_df.columns]
            return new_df.to_dict('records'), new_cols

# save and store prepared DataTable
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
