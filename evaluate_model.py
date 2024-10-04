# evaluate_model.py
from sklearn.metrics import mean_squared_error

def evaluate_model(y_true, y_pred):
    return mean_squared_error(y_true, y_pred)
