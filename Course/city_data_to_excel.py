#I made an extra script to make a DataFrame that I could look at in Excel. 
#just for QA purposes. 
import pandas as pd
import sys
sys.path.append("C:\Users\Bill\Documents\data_vizualization\matplotlib")

from matplotlibFunctions import *  #I built some of my own matplotlib functions

city_data = load_data()  #using boston_housing.py

housing_features = city_data.data
housing_prices = city_data.target

df = pd.DataFrame(housing_features, index=housing_prices)

df.to_csv(r"C:\Users\Bill\OneDrive\Data Files\Courses_n_samplesets\boston_housing.csv",encoding="utf-8")


