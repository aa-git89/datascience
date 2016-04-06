import pandas as pd
import numpy as np

dtype_dict = {'bathrooms':float, 'waterfront':int, 'sqft_above':int, 'sqft_living15':float, \
              'grade':int, 'yr_renovated':int, 'price':float, 'bedrooms':float, 'zipcode':str, \
              'long':float, 'sqft_lot15':float, 'sqft_living':float, 'floors':float, 'condition':int, \
              'lat':float, 'date':str, 'sqft_basement':int, 'yr_built':int, 'id':str, 'sqft_lot':int, 'view':int}

df_housePrice_train = pd.read_csv("your_path/kc_house_data_small_train.csv", dtype = dtype_dict)
df_housePrice_test = pd.read_csv("your_path/kc_house_data_small_test.csv", dtype = dtype_dict)
df_housePrice_valid = pd.read_csv("your_path/kc_house_data_small_validation.csv", dtype = dtype_dict)
df_housePrice_full = pd.read_csv("your_path/kc_house_data_small.csv", dtype = dtype_dict)


def get_numpy_data(data_frame, features, output):
    data_frame["constant"] = 1.0
    features = ['constant'] + features

    feature_matrix = data_frame[features].as_matrix()
    output_sarray = np.array(output)

    output_array = output_sarray
    return feature_matrix, output_array

def normalize_features(features):
    norms_lst = []
    for i in range(0, np.shape(features)[1]):
        X = features[:,i]
        norms = np.linalg.norm(X, axis=0)
        X_normalized = X / norms
        features[:,i] = X_normalized
        norms_lst.append(norms)
    return (features, norms_lst)

feature_list = ['bedrooms',
                'bathrooms',
                'sqft_living',
                'sqft_lot',
                'floors',
                'waterfront',
                'view',
                'condition',
                'grade',
                'sqft_above',
                'sqft_basement',
                'yr_built',
                'yr_renovated',
                'lat',
                'long',
                'sqft_living15',
                'sqft_lot15']

features_train, output_train = get_numpy_data(df_housePrice_train, feature_list, df_housePrice_train['price'])
features_test, output_test = get_numpy_data(df_housePrice_test, feature_list, df_housePrice_train['price'])
features_valid, output_valid = get_numpy_data(df_housePrice_valid, feature_list, df_housePrice_train['price'])

features_train, norms = normalize_features(features_train) # normalize training set features (columns)
features_test = features_test / norms # normalize test set by training set norms
features_valid = features_valid / norms # normalize validation set by training set norms

distances = []

def compute_distances(features_instances, features_query):
    diff = features_train[0:len(features_instances[:,1])] - features_query
    for i in range(0, len((features_train[:,1]))):
        distances.append(np.sqrt(np.sum(diff[i]**2)))
    return distances

def k_nearest_neighbors(k, feature_train, features_query):
    distances = compute_distances(feature_train, features_query)
    neighbors = np.argsort(np.array(distances))
    return neighbors[0:k]

def predict_output_of_query(k, feature_train, output_train, features_query):
    neighbors = k_nearest_neighbors(k, feature_train, features_query)
    avg1 = 0
    for i in neighbors:
        #print "neigh for house", i
        avg1 += output_train["price"][i] #if I comment this .. code works and prints correct weights
    return avg1/k


pred_lst = []
for i in range(0,10):
    #print "run", i
    pred_lst.append(predict_output_of_query(10.0, features_train, df_housePrice_train, features_test[i]))
print pred_lst

#print pred_lst