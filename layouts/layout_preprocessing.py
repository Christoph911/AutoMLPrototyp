import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header

# define control panel for prepLayout
controls_prep = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.H5('Datensatz bearbeiten', style={'text-align': 'center'}),
                html.Hr(),
                html.H6('Spaltenoperationen', style={'text-align': 'center'}),
                dcc.Input(
                    id='add-column-name',
                    placeholder='Spaltenname eingeben',
                    value='',
                ),
                dcc.Input(
                    id='add-column-value',
                    placeholder='Spaltenwert eingeben',
                    value='',
                ), html.Br(),
                html.Button('Spalte hinzufügen', id='add_column_btn', style={'margin': 10}), html.Br(),
            ]
        ),
        dbc.FormGroup(
            [
                dcc.Input(
                    id='add-column-math-name',
                    placeholder='Spaltenname eingeben',
                    value='',
                ),
                dcc.Dropdown(
                    id='input-column-1'
                ),
                html.Div(id='input-column-1-div'),
                dcc.Dropdown(
                    id='operator',
                    options=[
                        {'label': '+', 'value': '+'},
                        {'label': '-', 'value': '-'},
                        {'label': '*', 'value': '*'},
                        {'label': '/', 'value': '/'}
                    ]
                ),
                # dbc.Input(id='input-column-2', type='number', value=0),
                dcc.Dropdown(
                    id='input-column-2'
                ),
                html.Div(id='input-column-2-div'),
                html.Button('Spalte hinzufügen mit Operation', id='add_column_math_btn'), html.Br(),
                html.Hr(),
            ]
        ),
        dbc.FormGroup(
            [
                dcc.Dropdown(
                    id='drop-column-1'
                ),
                html.Div(id='drop-column-1-div'),
                html.Button('Spalte entfernen', id='drop_column_btn'), html.Br(),

            ]
        ),

        dbc.FormGroup(
            [
                html.H6('Reihenoperationen', style={'text-align': 'center'}),
                dcc.Input(
                    id='add-row-value',
                    placeholder='Reihenwert eingeben',
                    value='',
                ), html.Br(),
                html.Button('Reihe hinzufügen', id='add_rows_btn'), html.Br(),
                dbc.Input(id='row-count', type='number'),
                html.Button('Reihe entfernen', id='drop_rows_btn'),
                html.Hr()
            ]
        ),
        dbc.FormGroup(
            [

                html.H6('Umgang mit Null-Values', style={'text-align': 'center'}),
                html.Button('Entferne Null-Values', id='drop_null_btn'),
                html.Button('Ersetze Null-Values mit Durchschnitt Spalte', id='replace_null_btn'), html.Br(),
                html.Hr(),

            ]
        ),
        dbc.FormGroup(
            [

                html.H6('Normalisieren', style={'text-align': 'center'}),
                html.Button('Z-Score', id='z_score_btn'),
                html.Button('Min-Max-Scaler', id='min_max_scaler_btn'),
                html.Button('Natürl. Logarithmus', id='log_btn'), html.Br(),
                html.Button('Label Encoding', id='label_encoding_btn'),
                html.Button('One Hot Encoding', id='hot_encoding_btn'),
                html.Hr(),
                dbc.Button('Änderungen speichern', id='save-table-changes-btn'),
            ]
        ),

    ]
)

# define card for table in prepLayout
card_table_prep = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label='Vorschau', tab_id='tab-1-prep'),
                ],
                id='card-tabs-prep',
                card=True,
                active_tab='tab-1-prep',
            )
        ),
        dbc.CardBody(
            html.Div([


                dbc.CardBody(id="table-prep"),

            ]),

        ),
    ]
)

layout_prep = dbc.Container(
    [
        html.Div(header),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_prep, md=4, align='start'),
                dbc.Col(card_table_prep, md=8, align='start'),
                dbc.Col(html.Div(id='data-prepared'), md=4, align='start')

            ]
        ),
    ],
    fluid=True,
)
