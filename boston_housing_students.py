"""
Loading the boston dataset and examining its target (label) distribution.
"""

# Load libraries
import numpy as np
import pylab as pl
from sklearn import datasets
from sklearn.tree import DecisionTreeRegressor

################################
### ADD EXTRA LIBRARIES HERE ###
################################

import numpy as np
from sklearn import cross_validation
from sklearn.metrics import  mean_squared_error
from sklearn.metrics import make_scorer
from sklearn.grid_search import GridSearchCV
from sklearn.neighbors import NearestNeighbors

'''Load the Boston dataset.'''
def load_data():

    boston = datasets.load_boston()
    return boston

'''Calculate the Boston housing statistics.'''
def explore_city_data(city_data):

    # Get the labels and features from the housing data
    housing_prices = city_data.target
    housing_features = city_data.data

    ###################################
    ### Step 1. YOUR CODE GOES HERE ###
    ###################################

    data_size = housing_prices.size
    count_features = city_data.feature_names.size
    minimum_value = housing_prices.min()
    maximum_value = housing_prices.max()
    mean = np.mean(housing_prices)
    median = np.median(housing_prices)
    sdev = np.std(housing_prices)

    print {
        "Size of data": data_size,
        "Number of features": count_features,
        "Minimum value": minimum_value,
        "Maximum value": maximum_value,
        "Mean": mean,
        "Median": median,
        "Standard deviation": sdev
    }

    # Please calculate the following values using the Numpy library
    # Size of data?
    # Number of features?
    # Minimum value?
    # Maximum Value?
    # Calculate mean?
    # Calculate median?
    # Calculate standard deviation?


'''Calculate and return the appropriate performance metric.'''
def performance_metric(label, prediction):

    ###################################
    ### Step 2. YOUR CODE GOES HERE ###
    ###################################

    # http://scikit-learn.org/stable/modules/classes.html#sklearn-metrics-metrics

    return mean_squared_error(label, prediction)

    pass


'''Randomly shuffle the sample set. Divide it into training and testing set.'''
def split_data(city_data):

    # Get the features and labels from the Boston housing data
    X, y = city_data.data, city_data.target

    ###################################
    ### Step 3. YOUR CODE GOES HERE ###
    ###################################

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.33, random_state=42)

    return X_train, y_train, X_test, y_test


'''Calculate the performance of the model after a set of training data.'''
def learning_curve(depth, X_train, y_train, X_test, y_test):

    # We will vary the training set size so that we have 50 different sizes
    sizes = np.linspace(1, len(X_train), 50)
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


'''Plot training and test error as a function of the training size.'''
def learning_curve_graph(sizes, train_err, test_err):

    pl.figure()
    pl.title('Decision Trees: Performance vs Training Size')
    pl.plot(sizes, test_err, lw=2, label = 'test error')
    pl.plot(sizes, train_err, lw=2, label = 'training error')
    pl.legend()
    pl.xlabel('Training Size')
    pl.ylabel('Error')
    pl.show()


'''Calculate the performance of the model as model complexity increases.'''
def model_complexity(X_train, y_train, X_test, y_test):

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


'''Plot training and test error as a function of the depth of the decision tree learn.'''
def model_complexity_graph(max_depth, train_err, test_err):

    pl.figure()
    pl.title('Decision Trees: Performance vs Max Depth')
    pl.plot(max_depth, test_err, lw=2, label = 'test error')
    pl.plot(max_depth, train_err, lw=2, label = 'training error')
    pl.legend()
    pl.xlabel('Max Depth')
    pl.ylabel('Error')
    pl.show()


'''Find and return the nearest neighbours of x in X'''
def find_nearest_neighbor_indexes(x, X):  # x is your vector and X is the data set.
   neigh = NearestNeighbors( n_neighbors = 10 )
   neigh.fit(X)
   distance, indexes = neigh.kneighbors(x)

   return indexes

'''Find and tune the optimal model. Make a prediction on housing data.'''
def fit_predict_model(city_data):

    # Get the features and labels from the Boston housing data
    X, y = city_data.data, city_data.target

    # Setup a Decision Tree Regressor
    regressor = DecisionTreeRegressor()

    parameters = {'max_depth':(1,2,3,4,5,6,7,8,9,10)}

    ###################################
    ### Step 4. YOUR CODE GOES HERE ###
    ###################################

    # 1. Find the best performance metric
    # should be the same as your performance_metric procedure
    # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html

    scorer = make_scorer(performance_metric, greater_is_better=False)

    # 2. Use gridearch to fine tune the Decision Tree Regressor and find the best model
    # http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html#sklearn.grid_search.GridSearchCV

    grid = GridSearchCV(regressor, parameters, scoring=scorer)
    grid.max_depth = 5

    # Fit the learner to the training data
    print "Final Model: "
    print grid.fit(X, y)
    
    # Use the model to predict the output of a particular sample
    x = np.array([11.95, 0.00, 18.100, 0, 0.6590, 5.6090, 90.00, 1.385, 24, 680.0, 20.20, 332.09, 12.13])
    _y = grid.predict(x)
    print "House: " + str(x)
    print "Prediction: " + str(_y)
    print "Best model parameter:  " + str(grid.best_params_)

    regressor.max_depth = grid.best_params_['max_depth']
    regressor.fit(X, y)
    prediction = regressor.predict(x)
    print "Price prediction with regressor: %s" % str(prediction)

    indexes = find_nearest_neighbor_indexes(x, X)
    sum_prices = []
    for i in indexes:
        sum_prices.append(city_data.target[i])

    neighbor_avg = np.mean(sum_prices)
    print "Nearest Neighbor Average: %s" % str(neighbor_avg)


'''Analyze the Boston housing data. Evaluate and validate the
    performanance of a Decision Tree regressor on the Boston data.
    Fine tune the model to make prediction on unseen data.'''
def main():

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
    # # #
    # # Model Complexity Graph
    model_complexity(X_train, y_train, X_test, y_test)
    #
    # # Tune and predict Model
    fit_predict_model(city_data)


main()