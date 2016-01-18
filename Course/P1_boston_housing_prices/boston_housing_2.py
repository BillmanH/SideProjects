"""Load the Boston dataset and examine its target (label) distribution."""

# Load libraries
import numpy as np
import pylab as pl
from sklearn import datasets
from sklearn.tree import DecisionTreeRegressor

################################
### ADD EXTRA LIBRARIES HERE ###
import math
import sklearn as sk
from sklearn import grid_search
from sklearn.metrics import fbeta_score, make_scorer
################################


def load_data():
    """Load the Boston dataset."""

    boston = datasets.load_boston()
    return boston


def explore_city_data(city_data):
	"""Calculate the Boston housing statistics."""

	# Get the labels and features from the housing data
	housing_prices = city_data.target
	housing_features = city_data.data

	###################################
	### Step 1. YOUR CODE GOES HERE ###
	print ("data contains "+str(np.size(city_data.target))+" houses")
	print ("each house has "+str(np.size(city_data.feature_names))+" features")
	print("Minimum value: "+str(np.min(city_data.target)))
	print("Maximum value: "+str(np.max(city_data.target)))
	print("Mean value: "+str(np.mean(city_data.target)))
	print("Median value: "+str(np.median(city_data.target)))
	print("Standard Deviation value: "+str(np.std(city_data.target)))
	###################################

	# Please calculate the following values using the Numpy library
	# Size of data (number of houses)?
	# Number of features?
	# Minimum price?
	# Maximum price?
	# Calculate mean price?
	# Calculate median price?
	# Calculate standard deviation?


def split_data(city_data):
	"""Randomly shuffle the sample set. Divide it into 70 percent training and 30 percent testing data."""
	# Get the features and labels from the Boston housing data
	X, y = city_data.data, city_data.target
	###################################
	### Step 2. YOUR CODE GOES HERE ###
	#note: in production change {{random_state=42}} to {{random_state=np.random.randint(1,100)}}
	X_train, X_test, y_train, y_test = sk.cross_validation.train_test_split(X, y, test_size=0.2, random_state=42)
	###################################
	return X_train, y_train, X_test, y_test


def performance_metric(label, prediction):
    """Calculate and return the appropriate error performance metric."""

    ###################################
    ### Step 3. YOUR CODE GOES HERE ###
    return sk.metrics.mean_squared_error(label,prediction)
	###################################


def learning_curve(depth, X_train, y_train, X_test, y_test):
	"""Calculate the performance of the model after a set of training data."""

	# We will vary the training set size so that we have 50 different sizes
	sizes = np.round(np.linspace(1, len(X_train), 50))
	train_err = np.zeros(len(sizes))
	test_err = np.zeros(len(sizes))

	print "Decision Tree with Max Depth: "
	print depth

	for i, s in enumerate(sizes):

		# Create and fit the decision tree regressor model
		regressor = DecisionTreeRegressor(max_depth=depth)
		regressor.fit(X_train[:s], y_train[:s])

		# Find the performance on the training and testing set
		train_err[i] = performance_metric(y_train[:s], regressor.predict(X_train[:s]))
		test_err[i] = performance_metric(y_test, regressor.predict(X_test))


	# Plot learning curve graph
	learning_curve_graph(sizes, train_err, test_err)


def learning_curve_graph(sizes, train_err, test_err):
    """Plot training and test error as a function of the training size."""

    pl.figure()
    pl.title('Decision Trees: Performance vs Training Size')
    pl.plot(sizes, test_err, color="blue", lw=2, label = 'test error')
    pl.plot(sizes, train_err, color="red", lw=2, label = 'training error')
    pl.legend()
    pl.xlabel('Training Size')
    pl.ylabel('Error')
    pl.show()


def model_complexity(X_train, y_train, X_test, y_test):
    """Calculate the performance of the model as model complexity increases."""

    print "Model Complexity: "

    # We will vary the depth of decision trees from 2 to 25
    max_depth = np.arange(1, 25)
    train_err = np.zeros(len(max_depth))
    test_err = np.zeros(len(max_depth))

    for i, d in enumerate(max_depth):
        # Setup a Decision Tree Regressor so that it learns a tree with depth d
        regressor = DecisionTreeRegressor(max_depth=d)

        # Fit the learner to the training data
        regressor.fit(X_train, y_train)

        # Find the performance on the training set
        train_err[i] = performance_metric(y_train, regressor.predict(X_train))

        # Find the performance on the testing set
        test_err[i] = performance_metric(y_test, regressor.predict(X_test))

    # Plot the model complexity graph
    model_complexity_graph(max_depth, train_err, test_err)


def model_complexity_graph(max_depth, train_err, test_err):
    """Plot training and test error as a function of the depth of the decision tree learn."""

    pl.figure()
    pl.title('Decision Trees: Performance vs Max Depth')
    pl.plot(max_depth, test_err, color="blue", lw=2, label = 'test error')
    pl.plot(max_depth, train_err, color="red", lw=2, label = 'training error')
    pl.legend()
    pl.xlabel('Max Depth')
    pl.ylabel('Error')
    pl.show()


def fit_predict_model(city_data):
	"""Find and tune the optimal model. Make a prediction on housing data."""

	# Get the features and labels from the Boston housing data
	X, y = city_data.data, city_data.target

	# Setup a Decision Tree Regressor
	regressor = DecisionTreeRegressor()

	parameters = {'max_depth':(1,2,3,4,5,6,7,8,9,10)}

	###################################
	### Step 4. YOUR CODE GOES HERE ###
	fit = regressor.fit(X, y)
	myScorer = make_scorer(sk.metrics.mean_squared_error, greater_is_better=False)
	reg = grid_search.GridSearchCV(fit,parameters,
									scoring=myScorer)
	reg.fit(city_data.data, city_data.target)
	###################################

	# 1. Find an appropriate performance metric. This should be the same as the
	# one used in your performance_metric procedure above:
	# http://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html

	# 2. We will use grid search to fine tune the Decision Tree Regressor and
	# obtain the parameters that generate the best training performance. Set up
	# the grid search object here.
	# http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html#sklearn.grid_search.GridSearchCV

	# Fit the learner to the training data to obtain the best parameter set
	print "Final Model: "
	print reg.fit(X, y)

	# Use the model to predict the output of a particular sample
	x = [11.95, 0.00, 18.100, 0, 0.6590, 5.6090, 90.00, 1.385, 24, 680.0, 20.20, 332.09, 12.13]
	y = reg.predict(x)
	print "House: " + str(x)
	print "Prediction: " + str(y)

def main():
    """Analyze the Boston housing data. Evaluate and validate the
    performanance of a Decision Tree regressor on the housing data.
    Fine tune the model to make prediction on unseen data."""

    # Load data
    city_data = load_data()

    # Explore the data
    explore_city_data(city_data)

    # Training/Test dataset split
    X_train, y_train, X_test, y_test = split_data(city_data)

    # Learning Curve Graphs
    max_depths = [1,2,3,4,5,6,7,8,9,10]
    for max_depth in max_depths:
        learning_curve(max_depth, X_train, y_train, X_test, y_test)

    # Model Complexity Graph
    model_complexity(X_train, y_train, X_test, y_test)

    # Tune and predict Model
    fit_predict_model(city_data)


if __name__ == "__main__":
    main()