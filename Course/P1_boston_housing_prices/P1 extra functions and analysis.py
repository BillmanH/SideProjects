#I made an extra script to make a DataFrame that I could look at in Excel. 
#just for QA purposes. 
import pandas as pd
import sys
sys.path.append("C:\Users\Bill\Documents\data_vizualization\matplotlib")

from matplotlibFunctions import *  #I built some of my own matplotlib functions
%matplotlib inline

city_data = load_data()  #using boston_housing.py

housing_features = city_data.data
housing_prices = city_data.target

df = pd.DataFrame(housing_features, index=housing_prices)

df.to_csv(r"C:\Users\Bill\OneDrive\Data Files\Courses_n_samplesets\boston_housing.csv",encoding="utf-8")


df = df.reset_index(drop=True)
df['MDEV'] = housing_prices = city_data.target
#LABEL YOUR DATA!
labels = ['CRIM','ZN','INDUS','CHAS','NOX','RM','AGE','DIS','RAD','TAX','PTRATIO','B','LSTAT','MDEV']
df.columns = labels

pairwiseCorelation(df)

for col in df.columns:
	print col
	x = df[col]
	singleVarHistogram(x,title=col)
	plt.show()
	
#run prediction 1000 times:
predictions = []
for i in range(1000):
	print 1000-i
	predictions.append(fit_predict_model(city_data))
	

singleVarHistogram(np.concatenate(predictions),title="1k Predictions")

df['isInRange'] = (df['MDEV'] > 20.5) & (df['MDEV'] < 22.5)
df[(df['MDEV'] > 20.5) & (df['MDEV'] < 22.5)]