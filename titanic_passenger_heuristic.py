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
predictions = {}
# Interpretation: This dictionary will hold the final heuristic in the form of passenger_id and values
#				  0 for not survived and 1 survived

df = pd.read_csv(titanic_data)
for passenger_index, passenger in df.iterrows():
	if(passenger.Sex == 'male'):
		predictions[passenger.PassengerId] = 0
	else:
		predictions[passenger.PassengerId] = 1
	
	if predictions[passenger.PassengerId] == passenger.Survived:
		nbr_predicted += 1
		
print 'Number of correctly perdicted is %s out of possible %s' %(nbr_predicted, len(df.index))
