import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import nav

# define control panel for prepLayout
controls_prep = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Button('Änderungen speichern/DropNull', id='save-table-changes-btn')
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
                dcc.Input(
                    id='add-column-name',
                    placeholder='Spaltennaamme eingeben',
                    value='',
                    style={'paadding': 10}
                ),
                html.Button('Spalte hinzufügen', id='add-column-btn', style={'margin': 10}),
                html.Div(id="table-prep"),
                html.Button('Reihe hinzufügen', id='add-rows-btn')

            ]),

        ),
    ]
)

layout_prep = dbc.Container(
    [
        html.H1('AutoML Prototyp - Preprocessing'),
        html.Div(nav),
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
