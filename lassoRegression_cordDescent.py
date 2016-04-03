import pandas as pd
import numpy as np
from math import log, sqrt
from sklearn import linear_model

dtype_dict = {'bathrooms':float, 'waterfront':int, 'sqft_above':int, 'sqft_living15':float, \
              'grade':int, 'yr_renovated':int, 'price':float, 'bedrooms':float, 'zipcode':str, \
              'long':float, 'sqft_lot15':float, 'sqft_living':float, 'floors':str, 'condition':int, \
              'lat':float, 'date':str, 'sqft_basement':int, 'yr_built':int, 'id':str, 'sqft_lot':int, 'view':int}

df_housePrice_train = pd.read_csv("C:/Amandeep/ML/Regression/kc_house_train_data.csv", dtype = dtype_dict)
df_housePrice_test = pd.read_csv("C:/Amandeep/ML/Regression/kc_house_test_data.csv", dtype = dtype_dict)

sales = pd.read_csv("C:/Amandeep/ML/Regression/kc_house_data.csv", dtype = dtype_dict)

def get_numpy_data(data_frame, features, output):
    data_frame["constant"] = 1.0
    features = ['constant'] + features

    feature_matrix = data_frame[features].as_matrix()
    output_sarray = np.array(output)

    output_array = output_sarray
    return feature_matrix, output_array


def predict_outcome(feature_matrix, weights):
    return np.dot(feature_matrix, weights)

def normalize_features(features):
    norms_lst = []
    for i in range(0, np.shape(features)[1] - 1):
        X = features[:,i + 1]
        norms = np.linalg.norm(X, axis=0)
        X_normalized = X / norms
        features[:,i + 1] = X_normalized
        norms_lst.append(norms)
    return (features, norms_lst)

def lasso_coordinate_descent_step(i, feature_matrix, output, weights, l1_penalty):
    # compute prediction
    ro = [0] * feature_matrix.shape[1]
    prediction = predict_outcome(feature_matrix, weights)
    # compute ro[i] = SUM[ [feature_i]*(output - prediction + weight[i]*[feature_i]) ]
    #for i in range(0, np.shape(feature_matrix)[i] - 1):
    ro[i] = sum(feature_matrix[:, i]*(output - prediction + weights[i]*feature_matrix[:, i]))
    if i == 0: # intercept -- do not regularize
        weights[i] = ro[i]
    elif ro[i] < -l1_penalty/2.:
        weights[i] = (ro[i] + l1_penalty/2)
    elif ro[i] > l1_penalty/2.:
        weights[i] = (ro[i] - l1_penalty/2)
    else:
        weights[i] = 0.

    return weights[i]

def lasso_cyclical_coordinate_descent(feature_matrix, output, initial_weights, l1_penalty, tolerance):
    repeat = True
    change = np.empty(len(initial_weights))
    while repeat:
    # create list to hold weight changes
    # use for loop to loop over all of the weights
    #    to update them
        print "ini weight", initial_weights
        for i in range(len(initial_weights)):
    # store the value of the old weight
            old_weight = initial_weights[i]
            initial_weights[i] = lasso_coordinate_descent_step(i, feature_matrix, output, initial_weights, l1_penalty)
            change[i] = old_weight - initial_weights[i]
        print "Change", change
        if np.max(change) < tolerance:
            repeat = False
    return initial_weights
      #   so you don't lose it
      # update this weight by calling the
      #   lasso_coordinate_descent_step() function
      # add the weight CHANGE to your list of weight changes
      # check to see if the maximum weight change
      #    is less than the tolerance
      #    if so, exit the loop
    return the_updated_weights

simple_features = ['sqft_living', 'bedrooms']
my_output= sales['price']
(simple_feature_matrix, output) = get_numpy_data(sales, simple_features, my_output)
#print simple_feature_matrix[:,1]
#print simple_feature_matrix
norms_features, norms_lst = normalize_features(simple_feature_matrix)
#print norms_features, norms_lst
initial_weights = np.array([0.0,0.0,0.0])
l1_penalty = 1e7
tolerance = 1.0

fin_weights = lasso_cyclical_coordinate_descent(norms_features, output, initial_weights, l1_penalty, tolerance)
print fin_weights
#fm = predict_outcome(norms_features, initial_weights)
#print fm

# should print 0.425558846691
#import math
#print lasso_coordinate_descent_step(1, np.array([[3./math.sqrt(13),1./math.sqrt(10)],
#                   [2./math.sqrt(13),3./math.sqrt(10)]]), np.array([1., 1.]), np.array([1., 4.]), 0.1)
