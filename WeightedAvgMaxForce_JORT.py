import pandas as pd
import numpy as np

# This script is to create a weighted average for each participant for the JORT data

df = pd.read_excel('S3_jort_results_max_force_points_TrialN.xlsx') #loads in excel file as DataFrame


df['Participant_ID'] = df['Participant_ID'].str[:-2] #strips A and B (i.e. last 2 characters) off the end of the participant ID so identical values presented


grouped = df.groupby('Participant_ID') #groups identical values in Participant_ID column
getweightavgmax0 = lambda g: np.average(g['Max_0points'], weights=g['TrialN_0']) # calculates weighted average (weighted by Trial Number completed) for 0 point trials 
getweightavgmax10 = lambda g: np.average(g['Max_10points'], weights=g['TrialN_10']) # calculates weighted average (weighted by Trial Number completed) for 10 point trials
getweightavgmax100 = lambda g: np.average(g['Max_100points'], weights=g['TrialN_100']) ## calculates weighted average (weighted by Trial Number completed) for 100 point trials
getweightavgmax1000 = lambda g: np.average(g['Max_1000points'], weights=g['TrialN_1000'])## calculates weighted average (weighted by Trial Number completed) for 1000 point trials
#print(grouped.apply(getweightavg))

max_0 = grouped.apply(getweightavgmax0) #applies weighted average to grouped data (single participant) for 0 point trials
max_10 = grouped.apply(getweightavgmax10) #applies weighted average to grouped data (single participant) for 10 point trials
max_100 = grouped.apply(getweightavgmax100) #applies weighted average to grouped data (single participant) for 100 point trials
max_1000 = grouped.apply(getweightavgmax1000) #applies weighted average to grouped data (single participant) for 1000 point trials

#subtracting -  1000 point trial minus 100, 10 and 0 points
sub1000_100 = max_1000 - max_100
sub1000_10 = max_1000 - max_10
sub1000_0 = max_1000 - max_0

#subtracting - 100 point trial minus 10 and 0 
sub100_10 = max_100 - max_10
sub100_0 = max_100 - max_0

#subtracting - 10 point trial minus 0 
sub10_0 = max_10 - max_0

data = pd.DataFrame([max_0, max_10, max_100, max_1000, sub1000_100, sub1000_10, sub1000_0, sub100_10, sub100_0, sub10_0]) #creates a new data frame containing new weighted values
data_transposed = data.T #changes from row to column format
data_transposed.columns = ['0_points', '10_points', '100_points', '1000_points', 'sub1000minus100', 'sub1000minus10', 'sub1000minus0', 'sub100minus10', 'sub100minus0', 'sub10minus0'] #adds a label to each column

data_transposed.to_excel("S3_JORT_MaxPoints.xlsx") #saves data into an excel form


