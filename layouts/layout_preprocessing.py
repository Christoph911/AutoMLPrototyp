import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header

# define control panel for prepLayout
controls_prep = dbc.Card(
    [
        dbc.FormGroup(
            [
                dcc.Input(
                    id='add-column-name',
                    placeholder='Spaltenname eingeben',
                    value='',
                    style={'paadding': 10}
                ),
                dcc.Input(
                    id='add-column-value',
                    placeholder='Spaltenwert eingeben',
                    value='',
                    style={'paadding': 10}
                ),html.Br(),
                html.Button('Spalte hinzufügen', id='add_column_btn', style={'margin': 10}),html.Br(),
                html.Hr(),
                dcc.Input(
                    id='add-row-value',
                    placeholder='Reihenwert eingeben',
                    value='',
                    style={'paadding': 10}
                ),html.Br(),
                html.Button('Reihe hinzufügen', id='add_rows_btn'),html.Br(),
                html.Hr(),
                dbc.Input(id='input-column-1', type='number', value=0),
                dcc.Dropdown(
                    id='operator',
                    options=[
                        {'label': '+', 'value': '+'},
                        {'label': '-', 'value': '-'},
                        {'label': '*', 'value': '*'},
                        {'label': '/', 'value': '/'}
                    ]
                ),
                dbc.Input(id='input-column-2', type='number', value=0),
                html.Button('Spalte hinzufügen mit Operation', id='add_column_math_btn'),html.Br(),
                html.Hr(),
                html.Button('Entferne Null-Values',id='remove-null-btn'),html.Br(),
                html.Hr(),
                dbc.Button('Änderungen speichern', id='save-table-changes-btn'),
            ]
        )
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


                html.Div(id="table-prep"),

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
        )
    ],
    fluid=True,
)
