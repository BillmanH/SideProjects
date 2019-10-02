# Import libraries
from sklearn import preprocessing
from sklearn.metrics import make_scorer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from __future__ import division
import sklearn as sk
from sklearn import grid_search
from sklearn.metrics import f1_score

# loading student data from local file.
student_data = pd.read_csv(
    r"C:\Users\Bill\Documents\Statistics\Course\P2_Student_Intervention_System\student_intervention\student-data.csv")

n_students = len(student_data)  # assuming that all rows are students
# passed is the target, so it isn't counted as a feature
n_features = len(student_data.columns[student_data.columns != "passed"])
n_passed = len(student_data[student_data['passed'] == 'yes'])
# arbitrarily calling students who are (passed!="yes") as 'failed'
n_failed = len(student_data[student_data['passed'] != 'yes'])
grad_rate = n_passed/len(student_data)
print "Total number of students: {}".format(n_students)
print "Number of students who passed: {}".format(n_passed)
print "Number of students who failed: {}".format(n_failed)
print "Number of features: {}".format(n_features)
print "Graduation rate of the class: {:.2f}%".format(grad_rate)

# Extract feature (X) and target (y) columns
# all columns but last are features
feature_cols = list(student_data.columns[:-1])
target_col = student_data.columns[-1]  # last column is the target/label
print "Feature column(s):-\n{}".format(feature_cols)
print "Target column: {}".format(target_col)

X_all = student_data[feature_cols]  # feature values for all students
y_all = student_data[target_col]  # corresponding targets/labels
print "\nFeature values:-"
print X_all.head()  # print the first 5 rows

# Preprocess feature columns


def preprocess_features(X):
    outX = pd.DataFrame(index=X.index)  # output dataframe, initially empty

    # Check each column
    for col, col_data in X.iteritems():
        # If data type is non-numeric, try to replace all yes/no values with 1/0
        if col_data.dtype == object:
            col_data = col_data.replace(['yes', 'no'], [1, 0])
        # Note: This should change the data type for yes/no columns to int

        # If still non-numeric, convert to one or more dummy variables
        if col_data.dtype == object:
            # e.g. 'school' => 'school_GP', 'school_MS'
            col_data = pd.get_dummies(col_data, prefix=col)

        outX = outX.join(col_data)  # collect column(s) in output dataframe

    return outX


X_all = preprocess_features(X_all)
print "Processed feature columns ({}):-\n{}".format(len(X_all.columns), list(X_all.columns))

# First, decide how many training vs test samples you want
num_all = student_data.shape[0]  # same as len(student_data)
num_train = 300  # about 75% of the data
num_test = num_all - num_train

# TODO: Then, select features (X) and corresponding labels (y) for the training and test sets
# Note: Shuffle the data or randomly select samples to avoid any bias due to ordering in the dataset
# X_train = X_all[:num_train]
# y_train = y_all[:num_train]
# X_test = X_all[num_train:]
# y_test = y_all[num_train:]
X_train, X_test, y_train, y_test = sk.cross_validation.train_test_split(
    X_all, y_all, train_size=num_train, random_state=42)
print "Training set: {} samples".format(X_train.shape[0])
print "Test set: {} samples".format(X_test.shape[0])
# Note: If you need a validation set, extract it from within training data

# Train a model


def train_classifier(clf, X_train, y_train):
    print "Training {}...".format(clf.__class__.__name__)
    start = time.time()
    clf.fit(X_train, y_train)
    end = time.time()
    print "Done!\nTraining time (secs): {:.3f}".format(end - start)

# TODO: Choose a model, impfort it and instantiate an object


def predict_labels(clf, features, target):
    print "Predicting labels using {}...".format(clf.__class__.__name__)
    start = time.time()
    y_pred = clf.predict(features)
    end = time.time()
    print "Done!\nPrediction time (secs): {:.3f}".format(end - start)
    return f1_score(target.values, y_pred, pos_label='yes')

# Train and predict using different training set sizes


def train_predict(clf, X_train, y_train, X_test, y_test):
    print "------------------------------------------"
    print "Training set size: {}".format(len(X_train))
    train_classifier(clf, X_train, y_train)
    print "F1 score for training set: {}".format(predict_labels(clf, X_train, y_train))
    print "F1 score for test set: {}".format(predict_labels(clf, X_test, y_test))

# I made my own function to pull out the table for the report.


def train_predict_many(clf, X_train, y_train, X_test, y_test, results):
        # tweaked to return a dataframe of results for graphing.
        #
    train_start = time.time()
    train_classifier(clf, X_train, y_train)
    train_end = time.time()
    #
    predict_start = time.time()
    prediction = predict_labels(clf, X_test, y_test)
    predict_end = time.time()
    #
    index_n = len(results)
    results.loc[index_n, "train_f1"] = predict_labels(clf, X_train, y_train)
    results.loc[index_n, "test_f1"] = prediction
    results.loc[index_n, "train_size"] = len(X_train)
    results.loc[index_n, "train_time"] = train_end - train_start
    results.loc[index_n, "prediction_time"] = predict_end - predict_start


def test_my_model(clf, X_all, y_all, training_sizes):
    results = pd.DataFrame()
    for size in training_sizes:
        # removed test so that model will differ to the global X_test and y_test variables.
        X_train, X_test_not_used, y_train, y_test_not_used = sk.cross_validation.train_test_split(
            X_all, y_all, train_size=size, random_state=42)
        train_predict_many(clf, X_train, y_train, X_test, y_test, results)
        results.index = results['train_size']
    return results


# using the same training sizes for each model:
training_sizes = [100, 200, 300]

# running each Model separatley:


# DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state=0)
DecisionTree_results = test_my_model(clf, X_all, y_all, training_sizes)

# RandomForestClassifier
clf = RandomForestClassifier(random_state=0)
RandomForest_results = test_my_model(clf, X_all, y_all, training_sizes)

# KNeighborsClassifier
clf = KNeighborsClassifier()
KNeighbors_results = test_my_model(clf, X_all, y_all, training_sizes)


# graphing the different models to look at which one is more reliable.
plt.plot(KNeighbors_results['train_size'].tolist(
), KNeighbors_results['test_f1'].tolist(), label='KNeighbors')
plt.plot(RandomForest_results['train_size'].tolist(
), RandomForest_results['test_f1'].tolist(), label='RandomForest')
plt.plot(DecisionTree_results['train_size'].tolist(
), DecisionTree_results['test_f1'].tolist(), label='DecisionTree')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1))
plt.xlabel('Training Size')
plt.ylabel('F1 score')
plt.show()


X_train, X_test, y_train, y_test = sk.cross_validation.train_test_split(
    X_all, y_all, train_size=300, random_state=42)

lb = preprocessing.LabelBinarizer()
lb.fit(y_train)
y_bin_train = np.array([number[0] for number in lb.fit_transform(y_train)])

lb_test = preprocessing.LabelBinarizer()
lb_test.fit(y_test)
y_test_bin = np.array([number[0] for number in lb_test.fit_transform(y_test)])

myScorer = make_scorer(f1_score, greater_is_better=True)
parameters = {'n_neighbors': range(5, 50)}

reg = grid_search.GridSearchCV(KNeighborsClassifier(), parameters,
                               scoring=myScorer)


reg.fit(X_train, y_bin_train)

print "Best model parameter:  " + str(reg.best_params_)
print "Best model score:  " + str(reg.best_score_)


clf = KNeighborsClassifier(n_neighbors=34)
KNeighbors_results_best = test_my_model(clf, X_all, y_all, training_sizes)

# graphing the different models to look at which one is more reliable.
# with the KNeighbors_results_best
plt.plot(KNeighbors_results_best['train_size'].tolist(
), KNeighbors_results_best['test_f1'].tolist(), label='KNeighbors_results_best')
plt.plot(KNeighbors_results['train_size'].tolist(
), KNeighbors_results['test_f1'].tolist(), label='KNeighbors')
plt.plot(RandomForest_results['train_size'].tolist(
), RandomForest_results['test_f1'].tolist(), label='RandomForest')
plt.plot(DecisionTree_results['train_size'].tolist(
), DecisionTree_results['test_f1'].tolist(), label='DecisionTree')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1))
plt.xlabel('Training Size')
plt.ylabel('F1 score')
plt.show()
