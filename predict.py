
import pickle
import numpy as np
model=pickle.load(open("model/stock_model.pkl","rb"))
def predict_next(o,h,l,v):
    return float(model.predict(np.array([[o,h,l,v]]))[0])
