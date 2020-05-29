import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header, zielwert_dropdown
# define control panel for modelLayout

#TODO: Dropdown ins masterlayout?
controls_linear_regression = dbc.Card(
        [   html.H5("Auswahlmenü", style={'text-align':'center'}),
            html.Hr(),
            zielwert_dropdown,
            dbc.FormGroup(
                [
                    dbc.Label('Train/Test-Size'),
                    dcc.Slider(
                        min=0.3,
                        max=0.8,
                        step=None,
                        marks={
                            0.3: '30%/70%', 0.4: '40%/60%', 0.5: '50%/50%',
                            0.6: '60%/40', 0.7: '70%/30%', 0.8: '80%/20%',
                        },
                        value=0.7,
                        id='train-test'
                    )
                ]
            ),
            html.Hr(),
            dbc.FormGroup(
                [
                    dbc.Label('Metriken auswählen:'),
                    dbc.Checklist(
                        options=[
                            {"label": "Mean absolute error", "value": 'mae'},
                            {"label": "Mean squared error", "value": 'mse'},
                            {"label": "Root mean squared error", "value": 'rmse'},
                        ],
                        value=[],
                        id='metrics',
                        switch=True
                    )
                ]
            ),
            html.Hr(),
            dbc.FormGroup(
                [
                    dbc.Button("Let the magic happen!", color="success", id="start-regression-btn"),
                ]
            ),
        ],
        body=True
    )

# define card for graph in modelLayout
card_graph_linear_regression = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Vorschau", tab_id="tab-1-reg"),
                    dbc.Tab(label="Metriken", tab_id="tab-2-reg"),
                    dbc.Tab(label='Feature Imp.', tab_id='tab-3-reg')
                ],
                id="card-tabs-model",
                card=True,
                active_tab="tab-1-reg",
            )
        ),
        dbc.CardBody(html.Div(id='tab-content'))
    ]
)

layout_linear_regression = dbc.Container(
    [
        html.Div(header),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_linear_regression, md=4, align="start"),
                dbc.Col(card_graph_linear_regression, md=8, align="start")

            ]
        )
    ],
    fluid=True,
)



