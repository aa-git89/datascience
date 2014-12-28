##########################################################
## Aim: Program to analyze data from 2014 Sochi olympics
## Start Date: 12/24/2014
## End Date: 
## Author: Amandeep Sharma
## References: U****.com, pandas 0.15.2 documentation,
##			   numpy 1.9 documentation
##########################################################

from pandas import DataFrame, Series
import pandas as pd
import numpy as np

###################################
## Data definition
###################################

countries = ['Russian Fed.', 'Norway', 'Canada', 'United States',
                 'Netherlands', 'Germany', 'Switzerland', 'Belarus',
                 'Austria', 'France', 'Poland', 'China', 'Korea', 
                 'Sweden', 'Czech Republic', 'Slovenia', 'Japan',
                 'Finland', 'Great Britain', 'Ukraine', 'Slovakia',
                 'Italy', 'Latvia', 'Australia', 'Croatia', 'Kazakhstan']
# Interpretation: countries is a list that consists of all the countries that were involved in sochi olympics

gold = [13, 11, 10, 9, 8, 8, 6, 5, 4, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
# Interpretation: gold is a list of gold medals in for various countries which in the order of the countries list

silver = [11, 5, 10, 7, 7, 6, 3, 0, 8, 4, 1, 4, 3, 7, 4, 2, 4, 3, 1, 0, 0, 2, 2, 2, 1, 0]
# Interpretation: silver is a list of silver medals in for various countries which in the order of the countries list

bronze = [9, 10, 5, 12, 9, 5, 2, 1, 5, 7, 1, 2, 2, 6, 2, 4, 3, 1, 2, 1, 0, 6, 2, 1, 0, 1]
# Interpretation: bronze is a list of bronze medals in for various countries which in the order of the countries list

olympic_medal_counts_df = DataFrame({'country_name':Series(countries),
                                         'gold':Series(gold), 'silver':Series(silver),
                                         'bronze':Series(bronze)})
# Interpretation: Contains the dataframe having countries, gold, silver and bronze as its parameters										 

avg_bronze_at_least_one_gold = np.average(olympic_medal_counts_df['bronze'], weights = (olympic_medal_counts_df['gold']>0))
# Interpretation: The data frame will contain the average bronze of all the countries with at least one gold

avg_medal_count = olympic_medal_counts_df[['gold','silver','bronze']][olympic_medal_counts_df['gold'] + \
					olympic_medal_counts_df['silver'] + olympic_medal_counts_df['bronze'] > 0].apply(np.mean)
# Interpretation: indicates the average number of gold, silver, and bronze medals earned amongst countries who earned 
# at least one medal of any kind at the 2014 Sochi olympics

points = np.dot(olympic_medal_counts_df[['gold','silver','bronze']],[4,2,1])
# Interpretation: Contains the points that each country earned during the games

olympic_points_df =  DataFrame({'country_name':Series(countries), 'points':points})
# Interpretation: This dataframe has the countries and the total points earned during the olympics
print olympic_points_df