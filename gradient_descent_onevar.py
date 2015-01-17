#################################################################################
## Aim: Program to perform gradient descent using one variable on housing data	#
##		in this case the predictor is number of rooms							#
## Date: 01/14/2015																#
## Author: Amandeep Sharma														#
## References: U****.com, pandas 0.15.2 documentation,							#	
##			   numpy 1.9 documentation											#
#################################################################################

# data set is present in this link: https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.data
# data set used is also present in my data folder under the name Housing_Prices

# importing all the required packages
import numpy
import pandas

########################################
## Data definition
########################################

housing_data = "Housing_Prices.csv" #Interpretation: housing_data is an variable that holds the csv file used for prediction
housing_df = pandas.read_csv(housing_data) #Interpretation: housing_df is a DataFrame which stores all 
#columns of housing data
values_ini = housing_df['MEDV'] #Interpretation: values_ini stores the actual value of the house as a Series
m = len(values_ini) * 1.0 #Interpretation: m holds the number of training set
housing_df['one'] = numpy.ones(m) #Adding a column to the DataFrame which will hold value one in all rows, 
#this is for the y intercept
predictors_ini = housing_df[['one', 'RM']] #Interpretation: predictors_ini is a DataFrame that holds the 
#predictors in this case the number of rooms
theta = numpy.zeros(len(predictors_ini.columns)) #Interpretation: theta holds the initial value of theta
predictors = numpy.array(predictors_ini) #Interpretation: predictors stores the predictors in array format
values = numpy.array(values_ini) #Interpretation: values stores the actual values in array format
alpha = 0.04 #Interpretation: alpha stores the learning rate
num_iterations = 100000 #Interpretation: num_iterations stores the number of iterations given for convergence

########################################
## Function definition
########################################

#compute_cost: Array, Array, Array -> Float
#Input: Predictor is a feature used to perform regression, values is the actual value of house, theta is the
#theta value
#Returns: The value of the cost function depending on the input values 
def compute_cost(predictors, values, theta):
    sum_of_square_errors = numpy.square(numpy.dot(predictors, theta) - values).sum()
    cost = sum_of_square_errors / (2*m)
    return cost
	
#gradient_descent: Array, Array, Array, Float, Integer -> Array, Series
#Input: Predictor is a feature used to perform regression, values is the actual value of house, theta is the
#theta value
#Returns: The final theta value and the history of cost function
def gradient_descent(predictors, values, theta, alpha, num_iterations):    
    cost_history = [] #Interpretation: Holds all the values of the cost function
    
    for i in range(0,num_iterations):
        cost = compute_cost(predictors, values, theta)
        cost_history.append(cost)
        theta = theta - alpha * (1/m) * numpy.dot((numpy.dot(predictors, theta) - values), predictors)

    return theta, pandas.Series(cost_history)

#calc_rsquared: Array, Array -> Float
#Input: predictors are the actual inputs and theta_fin is the final value of theta
#Returns: R^2
def calc_rsquared(predictors, theta_fin):
	predictions = numpy.dot(predictors, theta_fin)
	numerator = numpy.square(values - predictions).sum()
	mean = numpy.mean(values)
	denominator = numpy.square(values - mean).sum()
	r_squared = 1 - (numerator / denominator)
	return r_squared
	
theta_fin, cost_val = gradient_descent(predictors, values, theta, alpha, num_iterations)
print "The final value of theta is %s" %theta_fin
print "The history of cost values is %s" %cost_val
predictions = numpy.dot(predictors, theta_fin) #Interpretation: predictions holds the final predictions after
#getting the final value of theta 
r_squared = calc_rsquared(predictors, theta_fin)
print "R^2 is %s" %r_squared