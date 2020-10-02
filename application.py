import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from main import app, application
from layouts.layout_start import layout_start
from callbacks import *
from layouts.layout_upload import layout_upload
from layouts.layout_preprocessing import layout_prep
from layouts.layout_modellauswahl import layout_model
from layouts.layout_linear_regression import layout_linear_regression
from layouts.layout_kmeans import layout_kmeans
from layouts.layout_random_forest import layout_forest
from layouts.layout_neural_network import layout_nn
from layouts.layout_logistic_regression import layout_logistic_regression
from layouts.layout_forest_regressor import layout_forest_regressor
from layouts.layout_neural_network_classification import layout_nn_class

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # hidden Div for storing upload data as json
    dcc.Store(id='stored-data-upload'),
    # hidden Div for storing table-prep results as json
    dcc.Store(id='stored-data-prep'),
    dcc.Store(id='get-data-model'),
    # dcc Store to store figures as dict
    dcc.Store(id="store-figure-reg"),
    dcc.Store(id='store-figure-log'),
    dcc.Store(id='store-figure-forest'),
    dcc.Store(id='store-figure-forest-feat'),
    dcc.Store(id='store-figure-kmeans'),
    dcc.Store(id='store-figure-nn'),
    dcc.Store(id='store-figure-nn-reg'),
    dcc.Store(id='store-figure-feat'),
    dcc.Store(id='store-figure-forest-reg'),
    dcc.Store(id='store-figure-forest-reg-feat'),
    dcc.Store(id='store-figure-nn-class'),
    dcc.Store(id='store-figure-nn-class-metrics'),
    dcc.Store(id='store-fig-roc-log'),
    dcc.Store(id='store-figure-forest-roc'),
    dcc.Store(id='store-figure-nn-class-roc'),


    html.Div(id='page-content')
])

app.title = "Machine Learning Web-App"


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return layout_start
    elif pathname == '/upload':
        return layout_upload
    elif pathname == '/prep':
        return layout_prep
    elif pathname == '/model':
        return layout_model
    elif pathname == '/regression':
        return layout_linear_regression
    elif pathname == '/forest':
        return layout_forest
    elif pathname == '/forest_reg':
        return layout_forest_regressor
    elif pathname == '/kmeans':
        return layout_kmeans
    elif pathname == '/nn':
        return layout_nn
    elif pathname == '/log-regression':
        return layout_logistic_regression
    elif pathname == '/nn-class':
        return layout_nn_class
    else:
        return '404 - Hier gibt es nichts zu sehen!'


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True, port=8080)
