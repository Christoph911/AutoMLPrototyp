import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import json
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

tab1_layout = [html.Div("Storing data to hidden div and displaying as bar chart"),
               html.Button("Store data into hidden div",
                            n_clicks=0,
                            id='store-data-hidden-div'),
               html.Button("Display data from hidden div as bar chart",
                           n_clicks=0,
                           id='create-bar-chart'),
               dcc.Graph(id = "bar-graph")
               ]

tab2_layout = [html.Div("retrieving data from hidden div and displaying as line chart"),
               html.Button("Display data from hidden div as line chart",
                           n_clicks=0,
                           id='create-line-chart'),
               dcc.Graph(id = "line-graph")
               ]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
#app.config['suppress_callback_exceptions'] = True

## css file
#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    dcc.Location(id="url",refresh=False),
    # hidden Div for storing data needed for graphs
    html.Div(id='graph-data-json-dump', style={'display': 'none'}),
    # Title
    html.Div("Sharing data between callbacks"),

    # tabs
    # dcc.Tabs(id="tabs",value="1",children=[
    #     dcc.Tab(label="Tab 1", value="1"),
    #     dcc.Tab(label="Tab 2", value="2")]),

    dbc.Nav(id="tabs",
        children=[
            dbc.NavItem(dbc.NavLink("Tab 1",href="/")),
            dbc.NavItem(dbc.NavLink("Tab 2",href="/2"))
        ]
    ),



    # Tab-layout
    html.Div(id='tab-layout')
])

#switching between tabs
@app.callback(dash.dependencies.Output('tab-layout', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def call_tab_layout(pathname):
    if pathname == "/":
        return tab1_layout
    elif pathname == "/2":
        return tab2_layout
    else:
        return "404"

#sending data to hidden div from tab1
@app.callback(dash.dependencies.Output('graph-data-json-dump', 'children'),
              [dash.dependencies.Input('store-data-hidden-div', 'n_clicks')])
def store_data_to_hidden_div(nclick):
    if nclick == 0:
        raise PreventUpdate
    elif nclick >0:
        df = pd.DataFrame({'x_axis':[6,4,9],
                        'y_axis':[4,2,7]})
        return df.to_json(orient = 'split')

#plotting bar graph in same tab

@app.callback(dash.dependencies.Output('bar-graph', 'figure'),
              [dash.dependencies.Input('graph-data-json-dump', 'children'),
               dash.dependencies.Input('create-bar-chart', 'n_clicks')])
def create_bar_chart(json_dump, n_click):
    if n_click == 0:
        raise PreventUpdate

    elif n_click >0:
        json_dump = json.loads(json_dump)
        json_dump_df = pd.DataFrame(json_dump['data'], columns=json_dump['columns'])

        data = [go.Bar(
            x = json_dump_df['x_axis'].values,
            y = json_dump_df['y_axis'].values,
            name = "Bar Chart")]
        fig = go.Figure(data = data)
        return fig
    else:
        raise PreventUpdate

#plotting line graph in next tab
@app.callback(dash.dependencies.Output('line-graph', 'figure'),
              [dash.dependencies.Input('graph-data-json-dump', 'children'),
               dash.dependencies.Input('create-line-chart', 'n_clicks')])
def create_line_chart(json_dump, n_click):
    if n_click == 0:
        raise PreventUpdate

    elif n_click > 0:
        json_dump = json.loads(json_dump)
        json_dump_df = pd.DataFrame(json_dump['data'], columns=json_dump['columns'])

        data = [go.Scatter(
            x=json_dump_df['x_axis'].values,
            y=json_dump_df['y_axis'].values,
            name="Line Chart")]

        fig = go.Figure(data=data)
        return fig
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)