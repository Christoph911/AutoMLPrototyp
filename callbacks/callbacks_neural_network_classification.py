import os

# CAVE: stellt error Messages und warnings für TF aus!
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import json
from main import app
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from callbacks.callbacks_master import error_message_get_target
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras
import sklearn.metrics as metrics
from sklearn.metrics import f1_score, precision_score, recall_score


# get stored data, update dropdown, return selected target
@app.callback(
    [Output('zielwert-opt-nn-class', 'options'),
     Output('error-message-target-nn-class', 'children')],
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
    [Output('store-figure-nn-class', 'data'),
     Output('store-figure-nn-class-metrics', 'data'),
     Output('error-message-model-nn-class', 'children')],
    [Input('start-nn-class-btn', 'n_clicks')],
    [State('get-data-model', 'children'),
     State('zielwert-opt-nn-class', 'value'),
     State('optimizer-nn-class', 'value'),
     State('number-epochs-nn-class', 'value'),
     State('train-test-nn-class', 'value'),
     State('val-nn-class', 'value'),
     State('metrics-nn-class', 'value')]
)
def create_neural_network_classification(n_clicks, df, y, optimizer, number_epochs, train_test_size, validation_size, choose_metrics):
    try:
        # load data out of local storage and convert into dataFrame
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

        # create X and Y variables, store Y as 2D-Array
        Y = df[y]
        X = df.drop(y, axis=1)

        # encode class values as integers
        encoder = LabelEncoder()
        encoded_Y = encoder.fit_transform(Y)

        # min-max-scaler for encoded variables
        one_hot_y = keras.utils.to_categorical(
            encoded_Y, num_classes=None, dtype='float32'
        )

        # train-test-split function
        X_train, X_test, Y_train, Y_test = train_test_split(X, one_hot_y, train_size=train_test_size)

        # build model
        model = keras.Sequential(
            [
                keras.layers.Dense(8, input_dim=4, activation='relu'),
                keras.layers.Dense(10, activation='relu'),
                keras.layers.Dense(10, activation='relu'),
                keras.layers.Dense(10, activation='relu'),
                keras.layers.Dense(3, activation='softmax'),
            ]
        )

        # compile model
        model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

        # fit model
        history = model.fit(X_train, Y_train, epochs=number_epochs, verbose=2, validation_split=validation_size)

        # predict
        prediction = np.argmax(model.predict(X_test), axis=1)

        # convert predictions back into categorical values
        prediction_cat = encoder.inverse_transform(prediction)

        # convert Y_test back into categorical values
        Y_test_cat = np.argmax(Y_test, axis=1)
        Y_test_cat = encoder.inverse_transform(Y_test_cat)

        # get loss and accuracy
        train_loss = history.history['loss']
        train_accuracy = history.history['accuracy']
        val_loss = history.history['val_loss']
        val_accuracy = history.history['val_accuracy']

        # create metrics
        global recall, precision, f1

        # create metrics depends on user input
        if 'recall' in choose_metrics:
            recall = recall_score(Y_test_cat, prediction_cat, average='micro')
            recall = 'Recall Score: ' + str(recall.round(3))
        else:
            recall = None
        if 'precision' in choose_metrics:
            precision = precision_score(Y_test_cat, prediction_cat, average='micro')
            precision = 'Precision Score: ' + str(precision.round(3))
        else:
            precision = None
        if 'f1' in choose_metrics:
            f1 = f1_score(Y_test_cat, prediction_cat, average='micro')
            f1 = 'F1 Score: ' + str(f1.round(3))
        else:
            f1 = None


        # create figure for train loss and accuracy
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
            y=train_accuracy,
            mode='lines',
            name='Train Accuracy'

        ))

        fig.add_trace(go.Scatter(
            x=epochs,
            y=val_loss,
            mode='lines',
            name='Val loss'

        ))

        fig.add_trace(go.Scatter(
            x=epochs,
            y=val_accuracy,
            mode='lines',
            name='Val Accuracy'

        ))

        fig.update_layout(
            title='Train loss vs. Accuracy',
            xaxis_title='Epochen',
            yaxis_title='Loss/Accuracy',
            template='plotly_white'
        )

        # create confusion matrix
        confusion_matrix = metrics.confusion_matrix(Y_test_cat, prediction_cat)
        # convert results into int
        confusion_matrix = confusion_matrix.astype(int)
        # get target names
        target_names = Y.unique()
        # split target names by comma and return list
        target_names = ' '.join(target_names).split()

        # set variables for matrix
        z = confusion_matrix
        x = target_names
        y = target_names

        # change each element of z to type string for annotations
        z_text = [[str(y) for y in x] for x in z]

        # set up figure
        fig_class = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale='Blues')

        # add title and margin
        fig_class.update_layout(title_text='Confusion matrix',
                                margin=dict(t=50, l=200)
                                )
        # add colorbar
        fig_class['data'][0]['showscale'] = True

        return dict(figure=fig), dict(figure=fig_class), None

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
    Output("tab-content-nn-class", "children"),
    [Input("card-tabs-nn-class", "active_tab"),
     Input("store-figure-nn-class", "data"),
     Input('store-figure-nn-class-metrics', 'data')],
)
def create_tab_content(active_tab, data, data_class):
    if active_tab and data is not None:
        if active_tab == "tab-1-nn-class":
            figure = dcc.Graph(figure=data_class["figure"])
            return figure
        elif active_tab == "tab-2-nn-class":
            figure = dcc.Graph(figure=data['figure'])
            return figure
        elif active_tab == "tab-3-nn-class":
            return recall, html.Br(), precision, html.Br(), f1, html.Br()
    return data
