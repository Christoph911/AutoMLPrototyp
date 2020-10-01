import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header

# define control panel for modelLayout

controls_forest = dbc.Card(
    [
        html.H5("Auswahlmenü", style={'text-align': 'center'}),
        html.Hr(),
        dbc.FormGroup(
            [
                dbc.Label("Zielwert"),
                dcc.Dropdown(
                    id="zielwert-opt-for",
                ),
                html.Div(id='zielwert-div'),
            ]
        ),
        dbc.FormGroup(
            [
                html.P("Anzahl Bäume:"),
                dbc.Input(id="number-trees", type="number", min=50, max=250, step=5, value=100)
            ],
        ),
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
                        {"label": "Recall Score", "value": 'recall'},
                        {"label": "Precision Score", "value": 'precision'},
                        {"label": "F1 Score", "value": 'f1'},
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
                dbc.Button("Start!", color="success", id="start-forest-btn"),
            ]
        ),
    ],
    body=True
)

# define card for graph in modelLayout
card_graph_forest = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label='Vorschau', tab_id='tab-1-forest'),
                    dbc.Tab(label='Metriken', tab_id='tab-2-forest'),
                    dbc.Tab(label='ROC-Curve', tab_id='tab-3-forest'),
                    dbc.Tab(label='Feature Imp.', tab_id='tab-4-forest')
                ],
                id='card-tabs-forest',
                card=True,
                active_tab='tab-1-forest',
            )
        ),
        dbc.CardBody(html.Div(id='tab-content-forest')),
    ]
)

layout_forest = dbc.Container(
    [
        html.Div(header),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_forest, md=4, align='start'),
                dbc.Col(card_graph_forest, md=8, align='start')
            ]
        ),
        html.Div(id='error-message-target-rf'),
        html.Div(id='error-message-model-rf')
    ],
    fluid=True,
)
