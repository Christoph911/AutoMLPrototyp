import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header

# define control panel for prepLayout
controls_columns = dbc.Card(
    [
        dbc.CardHeader("Spaltenoperationen"),

        dbc.FormGroup(
            [
                html.H6('Spalte erzeugen und mit Wert füllen:', style={'text-align': 'center'}),
                dcc.Input(
                    id='add-column-name',
                    placeholder='Spaltenname eingeben',
                    value='',

                ),
                dcc.Input(
                    id='add-column-value',
                    placeholder='Spaltenwert eingeben',
                    value='',
                ),
                dbc.Button('Spalte hinzufügen', id='add_column_btn', outline=True, color='secondary', size='sm', style={'margin':'8px'}),
                html.Hr(),
            ]
        ),
        dbc.FormGroup(
            [
                html.H6('Neue Spalte aus zwei bestehenden erzeugen:', style={'text-align': 'center'}),
                dcc.Input(
                    id='add-column-math-name',
                    placeholder='Spaltenname eingeben',
                    value='',
                ),
                dcc.Dropdown(
                    id='input-column-1',
                    placeholder='Spalte 1 auswählen'
                ),
                html.Div(id='input-column-1-div'),
                dcc.Dropdown(
                    id='operator',
                    options=[
                        {'label': '+', 'value': '+'},
                        {'label': '-', 'value': '-'},
                        {'label': '*', 'value': '*'},
                        {'label': '/', 'value': '/'}
                    ],
                    placeholder='Operation auswählen'
                ),

                dcc.Dropdown(
                    id='input-column-2',
                    placeholder='Spalte 2 auswählen'
                ),
                html.Div(id='input-column-2-div'),
                dbc.Button('Spalte hinzufügen mit Operation', id='add_column_math_btn', outline=True, color='secondary',
                           size='sm'),
                html.Hr(),
                dbc.FormGroup(
                    [
                        html.H6('Neue Spalte aus bestehnder und math. Operation:', style={'text-align': 'center'}),
                        dcc.Input(
                            id='add-column-math-name-2',
                            placeholder='Spaltenname eingeben',
                            value='',
                        ),
                        dcc.Dropdown(
                            id='create-column-math',
                            placeholder='Spalte auswählen'
                        ),
                        dcc.Dropdown(
                            id='operator-create-column',
                            options=[
                                {'label': '+', 'value': '+'},
                                {'label': '-', 'value': '-'},
                                {'label': '*', 'value': '*'},
                                {'label': '/', 'value': '/'}
                            ],
                            placeholder='Operation auswählen'
                        ),
                        dcc.Input(id="input-math", type="number", placeholder='Wert eingeben'),html.Br(),
                        dbc.Button('Spalte hinzufügen', id='create_column_math_btn', outline=True, color='secondary',
                                   size='sm'),
                        html.Hr(),

                    ]
                ),
                dbc.FormGroup(
                    [
                        html.H6('Spalte entfernen:', style={'text-align': 'center'}),
                        dcc.Dropdown(
                            id='drop-column-1',
                            multi=True,
                            placeholder='Spalte auswählen'
                        ),
                        html.Div(id='drop-column-1-div'),
                        dbc.Button('Spalte entfernen', id='drop_column_btn', outline=True, color='secondary',
                                   size='sm'),
                        html.Hr(),
                        html.H6('Werte nach Bedingung entfernen:', style={'text-align': 'center'}),
                        dcc.Dropdown(
                            id='column-operation',
                            options=[
                             {'label': 'drop', 'value': 'drop'}
                            ],
                            placeholder='Bedingung auswählen'
                         ),
                        dcc.Dropdown(
                            id='column-expression',
                            options=[
                            {'label': '>', 'value': '>'},
                            {'label': '>=', 'value': '>='},
                            {'label': '<', 'value': '<'},
                            {'label': '<=', 'value': '<='},
                            {'label': '=', 'value': '='}
                            ],
                            placeholder='Operation auswählen'
                        ),
                        dcc.Input(id="user-input", type="number", placeholder='Bedingung eingeben'),
                        dcc.Dropdown(
                            id='drop-column-expression-drp',
                            placeholder='Spalte auswählen'
                        ),

                        dbc.Button('Werte entfernen', id='drop_column_expr_btn', outline=True, color='secondary',
                                   size='sm'),
                    ]
                ),
            ]
        )
    ],
    color='secondary',
    outline=True,
    style={'margin-bottom': '10px'}
)

controls_rows = dbc.Card(
    [
        dbc.CardHeader("Reihenoperationen"),
        dbc.FormGroup(
            [
                html.H6('Reihe erzeugen und mit Wert füllen:', style={'text-align': 'center'}),
                dcc.Input(
                    id='add-row-value',
                    placeholder='Reihenwert eingeben',
                    value='',
                ),
                dbc.Button('Reihe hinzufügen', id='add_rows_btn', outline=True, color='secondary', size='sm', style={'margin': '8px'}), html.Br(),
                html.H6('Spalte entfernen:', style={'text-align': 'center'}),
                dcc.Input(id='row-count', type='number', placeholder='Nr. der Spalte wählen'),
                dbc.Button('Reihe entfernen', id='drop_rows_btn', outline=True, color='secondary', size='sm', style={'margin': '8px'}),
            ]
        )
    ],
    color='secondary',
    outline=True,
    style={'margin-bottom': '10px'}
)

controls_null = dbc.Card(
    [
        dbc.CardHeader("Null-Werte"),
        dbc.FormGroup(
            [
                html.H6('Null-Werte entfernen oder ersetzen:', style={'text-align': 'center'}),
                dcc.Dropdown(
                    id='dropNull-dropdown',
                    placeholder="Gesamter Datensatz",
                    multi=True
                ),
                html.Div(id='dropNull-dropdown-div'),
                dbc.Button('Entferne Null-Values', id='drop_null_btn', outline=True, color='secondary', size='sm'),
                dbc.Button('Ersetze Null-Values mit Durchschnitt Spalte', id='replace_null_btn', outline=True,
                           color='secondary', size='sm'), html.Br(),
            ],
        ),
    ],
    color='secondary',
    outline=True,
    style={'margin-bottom': '10px'}
)

controls_normalize = dbc.Card(
    [
        dbc.CardHeader("Normalisieren"),
        dbc.FormGroup(
            [
                html.H6('Datensatz normalisieren:', style={'text-align': 'center'}),
                dcc.Dropdown(
                    id='normalize-dropdown',
                    placeholder="Gesamter Datensatz",
                    multi=True
                ),
                html.Div(id='normalize-dropdown-div'),
                dbc.Button('Z-Score', id='z_score_btn', outline=True, color='secondary', size='sm'),
                dbc.Button('Min-Max-Scaler', id='min_max_scaler_btn', outline=True, color='secondary', size='sm'),
                dbc.Button('Natürl. Logarithmus', id='log_btn', outline=True, color='secondary', size='sm'), html.Br(),
                dbc.Button('Label Encoding', id='label_encoding_btn', outline=True, color='secondary', size='sm'),
            ],
        ),
    ],
    color='secondary',
    outline=True,
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
            [
                html.Div(id="table-prep"),
                dbc.Button("Geänderten Datensatz Speichern", id='save-table-changes-btn', style={'float': 'right'})
            ],
        ),

    ],
)

layout_prep = dbc.Container(
    [
        html.Div(header),
        dbc.Row(
            [
                dbc.Col([controls_columns, controls_rows, controls_null, controls_normalize], md=4, align='start'),
                dbc.Col(card_table_prep, md=8, align='start'),
                dbc.Col(html.Div(id='data-prepared'), md=4, align='start')

            ]
        ),

    ],
    fluid=True,
)
