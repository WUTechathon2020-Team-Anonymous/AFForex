import socket
import pickle
import numpy as np
from keras.models import model_from_json



def predict_rate(model, input_values, number_of_days):
    input_samples_number = 7
    input_samples = np.zeros((1, input_samples_number, 1))
    for i in range(input_samples_number):
        input_samples[0][i][0] = input_values[i]

    predicted_values = []
    for i in range(number_of_days):
        prediction = model.predict(input_samples, verbose=0)
        predicted_values.append(prediction[0][0])
        for j in range(input_samples_number-1):
            input_samples[0][j][0] = input_samples[0][j+1][0]
        input_samples[0][input_samples_number-1][0] = prediction[0][0]

    return predicted_values


ip = '192.168.1.11'
port = 4444
prediction_model_socket = socket.socket()
prediction_model_socket.bind((ip, port))
prediction_model_socket.listen()
# base_dir = 'C:\\Users\\Gautam\\Downloads\\CurrencyPrediction\\'

# load json and create model
file = open("EURUSDMODEL\\EURUSD", 'r')
model_json = file.read()
file.close()
eur = model_from_json(model_json)
# load weights
eur.load_weights("EURUSDMODEL\\EURUSDweights.h5")

file = open("INRUSDMODEL\\INRUSD", 'r')
model_json = file.read()
file.close()
inr = model_from_json(model_json)
# load weights
inr.load_weights("INRUSDMODEL\\INRUSDweights.h5")

file = open("AUDUSDMODEL\\AUDUSD", 'r')
model_json = file.read()
file.close()
aud = model_from_json(model_json)
# load weights
aud.load_weights("AUDUSDMODEL\\AUDUSDweights.h5")

file = open("GBPUSDMODEL\\GBPUSD", 'r')
model_json = file.read()
file.close()
gbp = model_from_json(model_json)
# load weights
gbp.load_weights("GBPUSDMODEL\\GBPUSDweights.h5")

# with open(base_dir+'INRUSD.pkl', 'rb') as inrfile:
#     inr = pickle.load(inrfile)
# with open(base_dir+'EURUSD.pkl', 'rb') as eurfile:
#     eur = pickle.load(eurfile)
# with open(base_dir+'GBPUSD.pkl', 'rb') as gbpfile:
#     gbp = pickle.load(gbpfile)
# with open(base_dir+'AUDUSD.pkl', 'rb') as audfile:
#     aud = pickle.load(audfile)

base_currency = 'usd'
currency_model_mapping = {'inr': inr, 'eur': eur, 'gbp': gbp, 'aud': aud}

while True:
    connected_socket, address = prediction_model_socket.accept()
    print('Connection :- ' + str(address))
    input_data = pickle.loads(connected_socket.recv(1024))
    input_data = list(input_data)
    currency_from = str(input_data.pop(0)).lower()
    currency_to = str(input_data.pop(0)).lower()
    print(currency_from)
    print(currency_to)
    number_of_days = input_data.pop()
    if currency_from == base_currency:
        value_from = [1] * number_of_days
    else:
        value_from = predict_rate(currency_model_mapping[currency_from], input_data, number_of_days)

    if currency_to == base_currency:
        value_to = [1] * number_of_days
    else:
        value_to = predict_rate(currency_model_mapping[currency_to], input_data, number_of_days)

    output_data = []
    for val_from, val_to in zip(value_from, value_to):
        output_data.append(val_to/val_from)

    print(output_data)
    connected_socket.send(pickle.dumps(output_data))
    connected_socket.close()
