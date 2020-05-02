import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from main import app
from callbacks import callbacks_upload, callbacks_preprocessing,callbacks_linear_regression,callbacks_kmeans,callbacks_random_forest, callbacks_neural_network


# define navbar for mainLayout
nav = dbc.Nav(
    children=[
        dbc.NavItem(dbc.NavLink("1. Daten hochladen", href='/upload')),
        dbc.NavItem(dbc.NavLink("2. Preprocessing", href='/prep')),
        dbc.NavItem(dbc.NavLink("3. Modellauswahl", href='/model')),
        dbc.NavItem(dbc.NavLink("4. Evaluation", href='/eval')),
    ],
    pills=True,
)

choose_model = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem('Supervised Learning', header=True),
        dbc.DropdownMenuItem('Lineare Regression', href='/regression'),
        dbc.DropdownMenuItem('Random Forest',href='/forest'),
        dbc.DropdownMenuItem('Unsupervised Learning', header=True),
        dbc.DropdownMenuItem('K-Means Clustering', href='/kmeans')
    ],
    label='Modellauswahl',
    bs_size='md',
),

header = (html.Div(children=[html.H1('Automated Machine Learning Web-App'),html.Img(src='/assets/images/logo.png',style={'position':'absolute','top':'0px','right':'0px','width':'170px','height':'100px','margin-top':'6px','margin-right':'12px'})]),
        html.Div(nav),
        html.Hr())

#METHOD NOT USED AT THE MOMENT
# nav = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("1. Daten hochladen", href='/upload')),
#         dbc.NavItem(dbc.NavLink("2. Preprocessing", href='/prep')),
#         dbc.NavItem(dbc.NavLink("3. Modellauswahl", href='/model')),
#         dbc.NavItem(dbc.NavLink("4. Evaluation", href='/eval')),
#     ],
#     brand="Automated Machine Learning Web-App",
#     brand_href="/",
#     color="primary",
#     dark=True,
#     expand='xl',
#     style={'height':'80px'}
# )