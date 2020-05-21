import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.masterlayout import header

layout_model = dbc.Container(
    [
        html.Div(header),
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [

                            dbc.Col(
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItemHeading('Supervised Learning',style={'text-align':'center'}),
                                        dbc.ListGroupItemText("Regression:"),
                                        dbc.ListGroupItem("Lineare Regression",action=True,href='/regression'),
                                        html.Br(),
                                        dbc.ListGroupItemText("Klassifikation:"),
                                        dbc.ListGroupItem('Logistische Regression',action=True,href='/log-regression'),
                                        dbc.ListGroupItem("Random Forest",action=True,href='/forest'),
                                    ],
                                )
                            ),
                            dbc.Col(
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItemHeading('Unsupervised Learning', style={'text-align':'center'}),
                                        dbc.ListGroupItemText("Clustering:"),
                                        dbc.ListGroupItem("K-Means Clustering",action=True,href='/kmeans')
                                    ],
                                )
                            ),
                            dbc.Col(
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItemHeading('Deep Learning', style={'text-align':'center'}),
                                        dbc.ListGroupItemText("Regression:"),
                                        dbc.ListGroupItem('Künstliches Neuronales Netz',action=True,href='/nn')
                                    ]
                                )
                            )
                        ]
                    ),
                ]
            )
        )
    ],
    fluid=True

)
