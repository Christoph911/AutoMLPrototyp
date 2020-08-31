import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from main import app
# TODO: Callbacks erst im spezifischen Layout Modul aufrufen? Performance?
from callbacks import callbacks_upload, callbacks_preprocessing, callbacks_linear_regression, callbacks_kmeans, \
    callbacks_random_forest, callbacks_neural_network, callbacks_logistic_regression, callbacks_random_forest_regressor, \
    callbacks_neural_network_classification, callbacks_master

# define navbar for mainLayout
nav = dbc.Nav(
    children=[
        dbc.NavItem(dbc.NavLink("1. Datensatz hochladen", href='/upload')),
        dbc.NavItem(dbc.NavLink("2. Datensatz bearbeiten", href='/prep')),
        dbc.NavItem(dbc.NavLink("3. Auswahl Machine Learning Model", href='/model'))
    ],
    pills=True,
)

header = (html.Div(children=[html.H1('Automated Machine Learning Web-App'), html.A([html.Img(
    src='/assets/images/logo.png',
    style={'position': 'absolute', 'top': '0px', 'right': '0px', 'width': '170px', 'height': '100px',
           'margin-top': '6px', 'margin-right': '12px'})], href='/')]),
          html.Div(nav),
          html.Hr())


