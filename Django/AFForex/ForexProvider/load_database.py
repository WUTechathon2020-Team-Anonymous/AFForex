from .models import Buy_Cash_Low, Buy_Cash_High, Buy_Card_Low, Buy_Card_High
from .models import Sell_Cash_Low, Sell_Cash_High, Sell_Card_Low, Sell_Card_High
from .models import Daily_Currencies_Value

from datetime import date, timedelta
import numpy as np

def load_min_max_table(currencies_name):
    history = np.array([
        [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  #26
         [74.4517, 76.72, 73.9525, 75.92, 70.92, 73.6534, 73.1688, 73.1688],
         [88.4632, 91.29, 88.1431, 90.45, 84.74, 87.5785, 87.2511, 87.2511],
         [98.9131, 102.22, 98.7898, 101.12, 95.08, 98.2558, 97.6944, 97.6944],
         [54.5667, 56.48, 54.4607, 55.96, 52.16, 54.0074, 53.8186, 53.8186]],
        [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # 25
         [74.4813, 76.89, 73.975, 76.044, 71.07, 73.6807, 73.259, 73.345],
         [88.3704, 91.3034, 88.1187, 90.453, 84.765, 87.3895, 87.2245, 87.135],
         [98.8785, 102.2633, 98.762, 101.21, 95.0973, 97.5734, 97.6481, 97.689],
         [50.5674, 56.4564, 54.4063, 55.9708, 51.71, 53.6832, 53.7102, 53.7102]],
        [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # 24
         [74.5013, 76.98, 74.075, 76.1344, 71.2107, 73.8077, 73.3889, 73.45],
         [88.2504, 91.34, 88.0308, 90.473, 84.65, 87.25, 87.1397, 87.035],
         [98.85, 102.33, 98.62, 101.27, 95.173, 97.4944, 97.5481, 97.684],
         [50.569, 56.464, 54.3273, 55.9715, 51.09, 53.2674, 53.6862, 53.582]],
        [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # 23
         [74.5609, 77.06, 74.23, 76.25, 71.25, 73.8795, 73.4442, 73.61],
         [87.8838, 91.31, 87.6661, 90.52, 84.51, 86.8893, 86.7704, 86.91],
         [98.7102, 102.41, 98.5381, 101.34, 95.28, 97.4654, 97.4521, 97.67],
         [50.59, 56.41, 54.0054, 55.9, 50.29, 52.9475, 53.3667, 53.45]],
        [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # 22
         [74.6213, 77.24, 74.275, 76.44, 71.07, 73.7743, 73.4889, 73.65],
         [88.387, 91.54, 88.06, 90.73, 84.65, 87.2594, 87.1397, 87.37],
         [98.8649, 102.33, 98.6423, 101.27, 94.73, 97.487, 97.5408, 97.87],
         [50.69, 56.64, 54.2976, 56.15, 50.09, 53.2154, 53.6346, 53.76]],
        [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # 21
         [74.6213, 77.24, 74.275, 76.44, 71.07, 73.7743, 73.4889, 73.65],
         [88.387, 91.54, 88.06, 90.73, 84.65, 87.2594, 87.1397, 87.37],
         [98.8649, 102.33, 98.6423, 101.27, 94.73, 97.487, 97.5408, 97.87],
         [50.69, 56.64, 54.2976, 56.15, 50.09, 53.2154, 53.6346, 53.76]],
        [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # 20
         [74.7758, 77.24, 74.275, 76.44, 71.07, 73.7743, 73.4889, 73.65],
         [88.3504, 91.54, 88.0308, 90.73, 84.65, 87.25, 87.1397, 87.35],
         [98.85, 102.33, 98.62, 101.27, 94.73, 97.4944, 97.5481, 97.84],
         [50.69, 56.64, 54.3273, 56.15, 50.09, 53.2674, 53.6862, 53.82]],
    ])

    today = date(2020, 11, 26)
    for i in range(7):
        obj, created = Buy_Cash_Low.objects.get_or_create(date=today - timedelta(days=i))
        for key, value in zip(currencies_name, history[i][:, 0]):
            setattr(obj.currencies, key, value)
        obj.save()

        obj, created = Buy_Cash_High.objects.get_or_create(date=today - timedelta(days=i))
        for key, value in zip(currencies_name, history[i][:, 1]):
            setattr(obj.currencies, key, value)
        obj.save()

        obj, created = Buy_Card_Low.objects.get_or_create(date=today - timedelta(days=i))
        for key, value in zip(currencies_name, history[i][:, 2]):
            setattr(obj.currencies, key, value)
        obj.save()

        obj, created = Buy_Card_High.objects.get_or_create(date=today - timedelta(days=i))
        for key, value in zip(currencies_name, history[i][:, 3]):
            setattr(obj.currencies, key, value)
        obj.save()

        obj, created = Sell_Cash_Low.objects.get_or_create(date=today - timedelta(days=i))
        for key, value in zip(currencies_name, history[i][:, 4]):
            setattr(obj.currencies, key, value)
        obj.save()

        obj, created = Sell_Cash_High.objects.get_or_create(date=today - timedelta(days=i))
        for key, value in zip(currencies_name, history[i][:, 5]):
            setattr(obj.currencies, key, value)
        obj.save()

        obj, created = Sell_Card_Low.objects.get_or_create(date=today - timedelta(days=i))
        for key, value in zip(currencies_name, history[i][:, 6]):
            setattr(obj.currencies, key, value)
        obj.save()

        obj, created = Sell_Card_High.objects.get_or_create(date=today - timedelta(days=i))
        for key, value in zip(currencies_name, history[i][:, 7]):
            setattr(obj.currencies, key, value)
        obj.save()

        print("From load min max table" + str(i))


def load_currency_history_table(currencies_name):
    history = np.array([
        [1, 73.86, 88.00, 98.63, 54.39], #26
        [1, 73.92, 87.9241, 98.7532, 54.3358], #25
        [1, 73.9641, 88.005, 98.838, 54.489], #24
        [1, 74.0308, 87.929, 98.955, 54.166], #23
        [1, 74.1305, 87.976, 98.639, 54.233], #22
        [1, 74.142, 87.935, 98.531, 54.159], #21
        [1, 74.165, 87.934, 98.521, 54.159], #20
    ])

    today = date(2020, 11, 26)
    for i in range(7):
        obj, created = Daily_Currencies_Value.objects.get_or_create(date=today - timedelta(days=i))
        for key, value in zip(currencies_name, history[i]):
            setattr(obj.currencies, key, value)
        obj.save()

        print("From load Currency Table" + str(i))


