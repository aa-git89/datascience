##########################################################################
## Aim: To write a heuristic that will use passengers' gender to predict   
##		if that person survived the titanic accident
## Start date: 12/28/2104
## Author: Amandeep Sharma
## References: U****.com, pandas 0.15.2 documentation,
##			   numpy 1.9 documentation
##########################################################################
import pandas as pd
import numpy as np
#import statsmodels.api as sm
import os

nbr_predicted = 0
# Interpretation: Holds the number of correctly guessed survival rate based on heuristic used
titanic_data = "C:/Python27/incoming/Intro-DataSc/titanic_data.csv"
# Interpretation: Holds the entire titanic dataset
predictions = {}
# Interpretation: This dictionary will hold the final heuristic in the form of passenger_id and values
#				  0 for not survived and 1 survived

# simple_heuristic: DataFrame -> Void
# Input: Passenger DataFrame, it has all the information of Titanic passengers
# Returns: If passenger is male then the dictionary key(which is the passengerId) us set to 0
#		   else it is set to 1
def simple_heuristic(passenger):
	if(passenger.Sex == 'male'):
		predictions[passenger.PassengerId] = 0
	else:
		predictions[passenger.PassengerId] = 1

# correct_simple_heuristic_prediction: DataFrame -> Void
# Returns: Increments the correct predictions if simple_heuristic predicts the actual outcome 
def correct_simple_heuristic_prediction(passenger):
	global nbr_predicted
	if predictions[passenger.PassengerId] == passenger.Survived:
		nbr_predicted += 1

df = pd.read_csv(titanic_data)

# simple_predictor: Void -> Void
def simple_predictor():
	for passenger_index, passenger in df.iterrows():
		simple_heuristic(passenger)
		correct_simple_heuristic_prediction(passenger)	

simple_predictor()		
print 'Number of correctly perdicted is %s out of possible %s' %(nbr_predicted, len(df.index))
