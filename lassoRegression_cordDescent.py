import pandas as pd
import numpy as np
from math import log, sqrt
from sklearn import linear_model

dtype_dict = {'bathrooms':float, 'waterfront':int, 'sqft_above':int, 'sqft_living15':float, \
              'grade':int, 'yr_renovated':int, 'price':float, 'bedrooms':float, 'zipcode':str, \
              'long':float, 'sqft_lot15':float, 'sqft_living':float, 'floors':float, 'condition':int, \
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
    for i in range(0, np.shape(features)[1]):
        X = features[:,i]
        norms = np.linalg.norm(X, axis=0)
        X_normalized = X / norms
        features[:,i] = X_normalized
        norms_lst.append(norms)
    return (features, norms_lst)

def lasso_coordinate_descent_step(i, feature_matrix, output, weights, l1_penalty):
    # compute prediction
    #ro = 0
    prediction = predict_outcome(feature_matrix, weights)
    #print "op and pred", output ,prediction
    # compute ro[i] = SUM[ [feature_i]*(output - prediction + weight[i]*[feature_i]) ]
    #for i in range(0, np.shape(feature_matrix)[i] - 1):
    ro = sum( feature_matrix[:, i] * (output - prediction + weights[i]*feature_matrix[:, i]) )
    #print "printing ro", ro, "lambda", l1_penalty/2
    if i == 0: # intercept -- do not regularize
        weights[i] = ro
    elif ro < -l1_penalty/2.:
        #print "increaing ro"
        weights[i] = ro + l1_penalty/2.
    elif ro > l1_penalty/2.:
        #print "decreasig ro"
        weights[i] = ro - l1_penalty/2.
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
        #print "ini weight", initial_weights
        for i in range(len(initial_weights)):
    # store the value of the old weight
            old_weight = initial_weights[i]
            initial_weights[i] = lasso_coordinate_descent_step(i, feature_matrix, output, initial_weights, l1_penalty)
            change[i] =  old_weight - initial_weights[i]
            #print "Change", change

        if np.max(change) < tolerance:
            #print "Entering if"
            repeat = False
    return initial_weights
      #   so you don't lose it
      # update this weight by calling the
      #   lasso_coordinate_descent_step() function
      # add the weight CHANGE to your list of weight changes
      # check to see if the maximum weight change
      #    is less than the tolerance
      #    if so, exit the loop

simple_features = ['sqft_living', 'bedrooms']
#simple_features = ['sqft_living']
my_output= sales['price']
(simple_feature_matrix, output) = get_numpy_data(sales, simple_features, my_output)
#print simple_feature_matrix[:,1]
#print simple_feature_matrix
#norms_features, norms_lst = normalize_features(simple_feature_matrix)
#print  norms_lst
#initial_weights = np.array([0.0,0.0,0.0])
#initial_weights = np.array([0., 0., 0.])
#l1_penalty = 1e7
#tolerance = 1.0

#fin_weights = lasso_cyclical_coordinate_descent(norms_features, output, initial_weights, l1_penalty, tolerance)
#print fin_weights
#fm = predict_outcome(norms_features, initial_weights)
#print fm

#sales["predict"] = model.predict(sales[['norm_sqft_living', 'norm_bedrooms']])
#rss = sum((sales["price"] - sales["predict"])**2)
#print rss
# should print 0.425558846691
#import math
#print lasso_coordinate_descent_step(1, np.array([[3./math.sqrt(13),1./math.sqrt(10)],
#                   [2./math.sqrt(13),3./math.sqrt(10)]]), np.array([1., 1.]), np.array([1., 4.]), 0.1)

#features, norms = normalize_features(np.array([[3.,6.,9.],[4.,8.,12.]]))
#print features
#print norms
#fin_wt = np.array([ 21624997.95951872,  63157247.20788978,         0.        ])
#print sum((output - predict_outcome(norms_features ,fin_wt))**2)

all_features = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront',\
                'view', 'condition', 'grade', 'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated']

my_output= df_housePrice_train['price']
(simple_feature_matrix, output) = get_numpy_data(df_housePrice_train, all_features, my_output)
#print simple_feature_matrix[:,1]
#print simple_feature_matrix
l1_penalty_7=1e7
l1_penalty_8=1e8
l1_penalty_4=1e4
tolerance=1.0
tolerance_4=5e5
norms_features, norms_lst = normalize_features(simple_feature_matrix)
#print norms_features
my_output_test= df_housePrice_test['price']
(simple_feature_matrix_test, output_test) = get_numpy_data(df_housePrice_test, all_features, my_output_test)

initial_weights = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
weights1e7 = lasso_cyclical_coordinate_descent(norms_features, output, initial_weights, l1_penalty_7, tolerance)
#print "Weigth 7 is", weights1e7
norm_wt_7 = weights1e7/norms_lst
print sum((output_test - predict_outcome(simple_feature_matrix_test ,norm_wt_7))**2)
weights1e8 = lasso_cyclical_coordinate_descent(norms_features, output, initial_weights, l1_penalty_8, tolerance)
#print "Weigth 8 is",weights1e8
norm_wt_8 = weights1e8/norms_lst
print sum((output_test - predict_outcome(simple_feature_matrix_test ,norm_wt_8))**2)
weights1e4 = lasso_cyclical_coordinate_descent(norms_features, output, initial_weights, l1_penalty_4, tolerance_4)
#print "Weigth 4 is", weights1e4
norm_wt_4 = weights1e4/norms_lst
print sum((output_test - predict_outcome(simple_feature_matrix_test ,norm_wt_4))**2)

