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
                                        dbc.ListGroupItemHeading('Supervised Learning'),
                                        dbc.ListGroupItem("Lineare Regression",action=True,href='/regression'),
                                        dbc.ListGroupItem("Random Forest",action=True,href='/forest'),
                                    ],
                                )
                            ),
                            dbc.Col(
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItemHeading('Unsupervised Learning'),
                                        dbc.ListGroupItem("K-Means Clustering",action=True,href='/kmeans')
                                    ],
                                )
                            ),
                        ]
                    ),
                ]
            )
        )
    ],
    fluid=True

)