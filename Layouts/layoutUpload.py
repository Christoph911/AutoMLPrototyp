import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Layouts.masterlayout import nav

# define control panel for uploadLayout
controls_upload = dbc.Card(
    [
        dbc.FormGroup(
            [
                dcc.Upload(
                    id="upload",
                    children=dbc.Button("Datensatz hochladen", color="secondary", outline=True, block=True),
                    multiple=True
                ),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Button("Zeige Vorschau an", id="start-preprocessing"),
            ]
        ),
    ]
)

# define card for table and metrics in uploadLayout
card_table_upload = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Vorschau", tab_id="tab-1"),
                    dbc.Tab(label="Infos", tab_id="tab-2"),
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(html.Div(id="table-head")),
    ]
)

layout_upload = dbc.Container(
    [
        html.H1("AutoML Prototyp - Daten hochladen"),
        html.Div(nav),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_upload, md=4, align="start"),
                dbc.Col(card_table_upload, md=8, align="start")
            ],

        )
    ],
    fluid=True,
)
