import numpy as np

def _predict_model(model, newdata):
    return np.array(model.predict(newdata)).flatten()
