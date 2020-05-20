import os
#CAVE: stellt error Messages und warnings für TF aus!
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import json
from main import app
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
import keras.backend.tensorflow_backend as tb
tb._SYMBOLIC_SCOPE.value = True


@app.callback(
    Output('zielwert-opt-nn', 'options'),
    [Input('load-data-nn','n_clicks')],
    [State('get-data-model', 'children')]
)
def update_date_dropdown(n_clicks, df):
    print("Daten an Dropdown Übergeben")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    options_y = [{'label': col, 'value': col} for col in df.columns]

    return options_y

@app.callback(
    [Output("store-figure-nn", "data"),
     Output('store-figure-nn-reg','data')],
    [Input('start-nn-btn', 'n_clicks')],
    [State('get-data-model', 'children'),
     State("zielwert-opt-nn", "value")]
)
def create_neural_network(n_clicks, df, y):
    print("started neural network")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    # MinMaxScaler for preprocessing
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_train = scaler.fit_transform(df)
    multiplied_by = scaler.scale_[13]
    added = scaler.min_[13]
    # store scaler results into dataFame
    scaled_train_df = pd.DataFrame(scaled_train, columns=df.columns.values)

    # get target column
    Y = scaled_train_df.loc[:, [y]]
    X = scaled_train_df.drop([y], axis=1).values

    # crate train/test and val seta
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.2)


    # build model
    model = keras.Sequential(
        [
            keras.layers.Dense(50,activation='relu'),
            keras.layers.Dense(100,activation='relu')
        ]
    )

    model.compile(optimizer='adam',loss='mean_squared_error', metrics=['mean_squared_error'])

    # fit model
    history = model.fit(X_train, Y_train, epochs=10, verbose=2, validation_data=(X_val, Y_val))

    # predict
    prediction = model.predict(X_train[:1])

    prediction_scaled_val = prediction - added
    print(prediction_scaled_val)
    #print('Prediction with scaling - {}'.format(prediction_scaled_val))
    prediction_norm_val = prediction / multiplied_by
    #print("Housing Price Prediction  - ${}".format(prediction_norm_val))



    # get scores

    #ACCURACY nur für Classification tasks
    train_loss = history.history['loss']
    #train_acc = history.history['accuracy']
    val_loss = history.history['val_loss']
    #val_acc = history.history['val_accuracy']
    val_mean_squared_error = history.history['val_mean_squared_error']


    # create figure for train and val loss

    epochs = list(range(1,11))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=epochs,
        y=train_loss,
        mode='lines',
        name='Train loss'

    ))
    fig.add_trace(go.Scatter(
        x=epochs,
        y=val_mean_squared_error,
        mode='lines',
        name='Val loss'

    ))

    fig.update_layout(
        title='Train loss vs. Val loss',
        xaxis_title='Epochen',
        yaxis_title='Loss',
        template='plotly_white'
    )
    # build figure
    fig_reg = go.Figure(
        data=[
            go.Scatter(
                x=Y_test,
                y=prediction_scaled_val,
                mode="markers",
                marker={"size": 8}
            )
        ]
    )
    fig_reg.update_layout(
        xaxis_title='Actual ',
        yaxis_title='Predict ',
        template='plotly_white'
    )

    return dict(figure=fig), dict(figure=fig_reg)

# manage tab content
@app.callback(
    Output("tab-content-nn", "children"),
    [Input("card-tabs-nn", "active_tab"),
     Input("store-figure-nn", "data"),
     Input('store-figure-nn-reg','data')],
)
def create_tab_content(active_tab, data, data_reg):
    if active_tab and data is not None:
        if active_tab == "tab-1-nn":
            figure = dcc.Graph(figure=data["figure"])
            return figure
        elif active_tab == "tab-2-nn":
            figure = dcc.Graph(figure=data_reg['figure'])
            return figure
    return data
