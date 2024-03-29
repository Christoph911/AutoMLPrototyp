import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header

test_modal = dbc.Modal(
    [
        dbc.ModalHeader("TEST"),
        dbc.ModalBody(["Fehlermeldung XY"]),
        dbc.ModalFooter("")
    ],
    is_open=True,
),


# define control panel for uploadLayout
controls_upload = dbc.Card(
    [

        dbc.FormGroup(
            [
                dcc.Upload(
                    id='upload',
                    children=dbc.Button('Datensatz hochladen', color='secondary', outline=True, block=True),
                    multiple=True
                )
            ]
        )
    ],
    color="light",
    outline=True
)

# define card for table and metrics in uploadLayout
card_table_upload = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label='Vorschau', tab_id='tab-1'),
                    dbc.Tab(label="Informationen", tab_id='tab-2'),
                    dbc.Tab(label="Korrelation", tab_id='tab-3'),
                    dbc.Tab(label="Histogram", tab_id='tab-4')
                ],
                id='card-tabs',
                card=True,
                active_tab='tab-1',
            )
        ),
        dbc.CardBody(html.Div(id='table-head')),
    ]
)

layout_upload = dbc.Container(
    [
        html.Div(header),
        dbc.Row(
            [
                dbc.Col(controls_upload, md=4, align='start'),
                dbc.Col(card_table_upload, md=8, align='start')
            ],
        ),
        html.Div(id='error-message-upload'),
    ],
    fluid=True,
)
