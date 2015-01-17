##########################################################################
## Aim: To write a heuristic that will use passengers' gender to predict   
##		if that person survived the titanic accident
## Start date: 12/28/2104
## Author: Amandeep Sharma
## References: U****.com, pandas 0.15.2 documentation,
##			   numpy 1.9 documentation
##########################################################################

# data set used is also present in my data folder under the name titanic_data

import pandas as pd
import numpy as np
#import statsmodels.api as sm
import os

########################################
## Data definition
########################################

sex_heu_predicted = 0
# Interpretation: Holds the number of correctly guessed survival rate based on sex heuristic used
sex_status_u18_predicted = 0
# Interpretation: Holds the number of correctly guessed survival rate based on sex or high class ticket and under 18 heuristic used
complex_predicted = 0
# Interpretation: Holds the number of correctly guessed survival rate based on complex heuristic used
titanic_data = "=titanic_data.csv"
# Interpretation: Holds the entire titanic dataset
predictions = {}
# Interpretation: This dictionary will hold the final heuristic in the form of passenger_id and values
#				  0 for not survived and 1 survived
df = pd.read_csv(titanic_data)

########################################
## Function definition
########################################

# sex_heuristic: DataFrame -> Void
# Input: Passenger DataFrame, it has all the information of Titanic passengers
# Returns: If passenger is male then the dictionary key(which is the passengerId) us set to 0
#		   else it is set to 1
def sex_heuristic(passenger):
	if(passenger.Sex == 'male'):
		predictions[passenger.PassengerId] = 0
	else:
		predictions[passenger.PassengerId] = 1

# correct_sex_heuristic_prediction: DataFrame -> Void
# Returns: Increments the correct predictions if sex_heuristic predicts the actual outcome 
def correct_sex_heuristic_prediction(passenger):
	global sex_heu_predicted
	if predictions[passenger.PassengerId] == passenger.Survived:
		sex_heu_predicted += 1

# sex_status_u18_heuristic: DataFrame -> Void
# Input: Passenger DataFrame, it has all the information of Titanic passengers
# Returns: If passenger is female or is under 18 and has a high status ticket 
# then the dictionary key(which is the passengerId) us set to 1		
def sex_status_u18_heuristic(passenger):
	if(passenger.Sex == 'female' or (passenger.Pclass == 1 and passenger.Age < 18)):
		predictions[passenger.PassengerId] = 1
	else:
		predictions[passenger.PassengerId] = 0
		
# correct_sex_heuristic_prediction: DataFrame -> Void
# Returns: Increments the correct predictions if sex_status_u18_heuristic predicts the actual outcome 
def correct_sex_status_u18_heuristic_prediction(passenger):
	global sex_status_u18_predicted
	if predictions[passenger.PassengerId] == passenger.Survived:
		sex_status_u18_predicted += 1

# complex_heuristic: DataFrame -> Void
# Input: Passenger DataFrame, it has all the information of Titanic passengers
# Returns: Predicts the survival rate based	complex conditions
def complex_heuristic(passenger):
	if(((passenger.Sex == 'female' or passenger.Age < 13) and passenger.Pclass < 3)\
		or (passenger.Pclass == 3 and passenger.Sex == 'female' and passenger.SibSp < 3)
		or (passenger.Sex == 'male' and passenger.Age < 15 and passenger.Pclass < 3)):
		predictions[passenger.PassengerId] = 1
	else:
		predictions[passenger.PassengerId] = 0

# correct_complex_prediction: DataFrame -> Void
# Returns: Increments the correct predictions based on complex condition 
def correct_complex_prediction(passenger):
	global complex_predicted
	if predictions[passenger.PassengerId] == passenger.Survived:
		complex_predicted += 1
		
# sex_predictor: Void -> Void
def sex_predictor():
	for passenger_index, passenger in df.iterrows():
		sex_heuristic(passenger)
		correct_sex_heuristic_prediction(passenger)	

# sex_status_u18_predictor: Void -> Void
def	sex_status_u18_predictor():
	for passenger_index, passenger in df.iterrows():
		sex_status_u18_heuristic(passenger)
		correct_sex_status_u18_heuristic_prediction(passenger)

def complex_predictor():
	for passenger_index, passenger in df.iterrows():
		complex_heuristic(passenger)
		correct_complex_prediction(passenger)
	
		
sex_predictor()
sex_status_u18_predictor()
complex_predictor()
print 'Number of correct predictions using sex heuristic is %s out of possible %s which is %s percent' %(sex_heu_predicted, len(df.index),\
	   format(sex_heu_predicted*100/len(df.index),'.2f'))
print 'Number of correct predictions using sex, age and status heuristic is %s out of possible %s which is %s percent' %(sex_status_u18_predicted, \
	   len(df.index), format(sex_status_u18_predicted*100/len(df.index),'.2f'))
print 'Number of correct predictions using complex heuristic is %s out of possible %s which is %s percent' %(complex_predicted, \
	   len(df.index), format(complex_predicted*100/len(df.index),'.2f'))	   