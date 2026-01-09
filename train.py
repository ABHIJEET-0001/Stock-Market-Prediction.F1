
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

df=pd.read_csv("data/TCS.csv")
X=df[['Open','High','Low','Volume']]
y=df['Close']
model=LinearRegression()
model.fit(X,y)
pickle.dump(model,open("model/stock_model.pkl","wb"))
print("Model trained")
