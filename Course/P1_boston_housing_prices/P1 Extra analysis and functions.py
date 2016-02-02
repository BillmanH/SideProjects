#I made an extra script to make a DataFrame that I could look at in Excel. 
#just for QA purposes. 
import pandas as pd
import sys
# Load libraries
import numpy as np
import pylab as pl
from sklearn import datasets
from sklearn.tree import DecisionTreeRegressor
import math
import sklearn as sk
from sklearn import grid_search
from sklearn.metrics import fbeta_score, make_scorer

sys.path.append("C:\Users\Bill\Documents\data_vizualization\matplotlib")

from matplotlibFunctions import *  #I built some of my own matplotlib functions
%matplotlib inline

#booting the boston_housing script:
sys.path.append("C:\Users\Bill\Documents\Statistics\Course\P1_boston_housing_prices")
import boston_housing_2


#Start Here:
city_data = boston_housing_2.load_data()  #using boston_housing.py

housing_features = city_data.data
housing_prices = city_data.target

#making a quick .csv to eyeball in Excel
df = pd.DataFrame(housing_features).reset_index(drop=True)
df['MDEV'] = housing_prices = city_data.target
labels = ['CRIM','ZN','INDUS','CHAS','NOX','RM','AGE','DIS','RAD','TAX','PTRATIO','B','LSTAT','MDEV']
df.columns = labels
df.to_csv(r"C:\Users\Bill\OneDrive\Data Files\Courses_n_samplesets\boston_housing.csv",encoding="utf-8")


pairwiseCorelation(df)

for col in df.columns:
	print col
	x = df[col]
	singleVarHistogram(x,title=col)
	plt.show()
	
	
#single commands to test output:
X, y = city_data.data, city_data.target
X_train, X_test, y_train, y_test = sk.cross_validation.train_test_split(X, y, test_size=0.3, random_state=42)

fit = regressor.fit(X, y)
myScorer = make_scorer(sk.metrics.mean_squared_error, greater_is_better=False)
reg = grid_search.GridSearchCV(fit,parameters,
								scoring=myScorer)
reg.fit(city_data.data, city_data.target)

boston_housing_2.learning_curve(1, X_train, y_train, X_test, y_test)

#run prediction 1000 times:
predictions = []
for i in range(1000):
	print 1000-i
	predictions.append(fit_predict_model(city_data))
	

singleVarHistogram(np.concatenate(predictions),title="1k Predictions")

df['isInRange'] = (df['MDEV'] > 20.5) & (df['MDEV'] < 22.5)
df[(df['MDEV'] > 20.5) & (df['MDEV'] < 22.5)]



from sklearn.neighbors import NearestNeighbors
x = [11.95, 0.00, 18.100, 0, 0.6590, 5.6090, 90.00, 1.385, 24, 680.0, 20.20, 332.09, 12.13]

 
   
indexes,distance = find_nearest_neighbor_indexes(x,X)

sum_prices = []
for i in indexes:
    sum_prices.append(city_data.target[i])

sum_prices = [city_data.target[i] for i in indexes]
	
neighbor_avg = np.mean(sum_prices)
print "Nearest Neighbors average: " +str(neighbor_avg)




boston_housing_2.main()