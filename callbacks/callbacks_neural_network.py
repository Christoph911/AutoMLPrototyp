import os

# CAVE: stellt error Messages und warnings für TF aus!
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import json
from main import app
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from callbacks.callbacks_master import error_message_get_target
import dash_bootstrap_components as dbc


# get stored data, update dropdown, return selected target
@app.callback(
    [Output('zielwert-opt-nn', 'options'),
     Output('error-message-target-nn', 'children')],
    [Input('get-data-model', 'children'),
     Input('zielwert-div', 'children')]
)
def get_target(df, dummy):
    try:
        print("Daten an Dropdown Übergeben")
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

        target = [{'label': col, 'value': col} for col in df.columns]

        return target, None
    except:
        return None, error_message_get_target


@app.callback(
    [Output("store-figure-nn", "data"),
     Output('store-figure-nn-reg', 'data'),
     Output('error-message-model-nn', 'children')],
    [Input('start-nn-btn', 'n_clicks')],
    [State('get-data-model', 'children'),
     State("zielwert-opt-nn", "value"),
     State('optimizer-nn', 'value'),
     State('number-epochs', 'value'),
     State('train-test-nn', 'value'),
     State('val-nn', 'value')]
)
def create_neural_network(n_clicks, df, y, optimizer, number_epochs, train_test_size, val_set_size):
    try:
        print("started neural network")
        # load data out of local storage and convert into dataFrame
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

        # create X and Y variables, store Y as 2D-Array
        Y = df[[y]]
        X = df.drop(y, axis=1)

        # split train and test set
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=train_test_size)

        # scale values
        scalerX = StandardScaler().fit(X_train)
        scalerY = StandardScaler().fit(Y_train)
        X_train = scalerX.transform(X_train)
        Y_train = scalerY.transform(Y_train)
        X_test = scalerX.transform(X_test)
        Y_test = scalerY.transform(Y_test)

        # build model
        model = keras.Sequential(
            [
                keras.layers.Dense(12, activation='relu'),
                keras.layers.Dense(8, activation='relu'),
                keras.layers.Dense(1, activation='linear')
            ]
        )

        model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['mean_squared_error'])

        # fit model
        history = model.fit(X_train, Y_train, epochs=number_epochs, verbose=2, validation_split=val_set_size)

        # predict
        prediction = model.predict(X_test)

        # scale back predicted and test values and store in 1D-Array
        prediction_norm_val = scalerY.inverse_transform(prediction).flatten()
        test_norm_val = scalerY.inverse_transform(Y_test).flatten()

        # get train and validation loss
        train_loss = history.history['loss']
        val_loss = history.history['val_loss']

        # create figure for train and val loss

        epochs = list(range(1, number_epochs + 1))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=epochs,
            y=train_loss,
            mode='lines',
            name='Train loss'

        ))

        fig.add_trace(go.Scatter(
            x=epochs,
            y=val_loss,
            mode='lines',
            name='Val loss'

        ))

        fig.update_layout(
            title='Train loss vs. Validation loss',
            xaxis_title='Epochen',
            yaxis_title='Loss',
            template='plotly_white'
        )

        # build figure for representation of predicted values
        fig_reg = go.Figure(
            data=[
                go.Scatter(
                    x=test_norm_val,
                    y=prediction_norm_val,
                    mode="markers",
                    marker={"size": 8}
                )
            ]
        )
        fig_reg.update_layout(
            xaxis_title='Actual ' + y,
            yaxis_title='Predict ' + y,
            template='plotly_white'
        )

        return dict(figure=fig), dict(figure=fig_reg), None

    except Exception as e:
        error_message_model = dbc.Modal(
            [
                dbc.ModalHeader("Fehler!"),
                dbc.ModalBody(["Es ist ein Fehler während des Trainingsprozesses aufgetreten:", html.Br(),
                               html.H6(str(e)), html.Br(),
                               " Bitte stell darüber hinaus sicher, dass der verwendete Datensatz keine Null-Values enthält "
                               "und das korrekte Modell für die Problemstellung ausgewählt wurde", html.Br(),
                               ]),
                dbc.ModalFooter("")
            ],
            is_open=True,
        )
        return None, None, error_message_model


# manage tab content
@app.callback(
    Output("tab-content-nn", "children"),
    [Input("card-tabs-nn", "active_tab"),
     Input("store-figure-nn", "data"),
     Input('store-figure-nn-reg', 'data')],
)
def create_tab_content(active_tab, data, data_reg):
    if active_tab and data is not None:
        if active_tab == "tab-1-nn":
            figure = dcc.Graph(figure=data_reg["figure"])
            return figure
        elif active_tab == "tab-2-nn":
            figure = dcc.Graph(figure=data['figure'])
            return figure
    return data
