import pandas as pd
import numpy as np

# This script is to create a weighted average for each participant for the JORT data_ Reaction Time Data

df = pd.read_excel('S3_jort_results_rt_points_TrialN.xlsx') #loads in excel file as DataFrame- reaction time data


df['Participant_ID'] = df['Participant_ID'].str[:-2] #strips A and B (i.e. last 2 characters) off the end of the participant ID so identical values presented


grouped = df.groupby('Participant_ID') #groups identical values in Participant_ID column
def getweightavg0(g):
    try:
        return np.average(g['RT_0points'], weights=g['Responded_0'])
    except ZeroDivisionError:
        return -9999
def getweightavg10(g):
    try:
        return np.average(g['RT_10points'], weights=g['Responded_10']) 
    except ZeroDivisionError:
        return -9999
def getweightavg100(g):
    try:
        return np.average(g['RT_100points'], weights=g['Responded_100'])
    except ZeroDivisionError:
        return -9999
def getweightavg1000(g):
    try:
        return np.average(g['RT_1000points'], weights=g['Responded_1000'])
    except ZeroDivisionError:
        return -9999

rt_0 = grouped.apply(getweightavg0) #applies weighted average to grouped data (single participant) for 0 point trials
rt_10 = grouped.apply(getweightavg10) #applies weighted average to grouped data (single participant) for 10 point trials
rt_100 = grouped.apply(getweightavg100) #applies weighted average to grouped data (single participant) for 100 point trials
rt_1000 = grouped.apply(getweightavg1000) #applies weighted average to grouped data (single participant) for 1000 point trials

#subtracting -  1000 point trial minus 100, 10 and 0 points
sub1000_100 = rt_1000 - rt_100
sub1000_10 = rt_1000 - rt_10
sub1000_0 = rt_1000 - rt_0

#Calculate above substractions only if values in each column not -9999 
sub1000_100 = sub1000_100.where((rt_100 != -9999) & (rt_1000 !=-9999), other = -9999) 
sub1000_10 = sub1000_10.where((rt_10 !=-9999) & (rt_1000 !=-9999), other = -9999)
sub1000_0 = sub1000_0.where((rt_0 != -9999) & (rt_1000 !=-9999), other = -9999) 

#subtracting - 100 point trial minus 10 and 0 points
sub100_10 = rt_100 - rt_10
sub100_0 = rt_100 - rt_0

#Calculate above only if values in 0 and 10 points not -9999
sub100_10 = sub100_10.where((rt_10 !=-9999) & (rt_100 !=-9999), -9999)
sub100_0 = sub100_0.where((rt_0 !=-9999) & (rt_100 !=-9999), -9999)

#subtracting - 10 point trial minus 0 
sub10_0 = rt_10 - rt_0

#Calculate above only if values in 0 and 10 points not -9999
sub10_0 = sub10_0.where((rt_10 !=-9999) & (rt_0 !=-9999), -9999)


data = pd.DataFrame([rt_0, rt_10, rt_100, rt_1000, sub1000_100, sub1000_10, sub1000_0, sub100_10, sub100_0, sub10_0]) #creates a new data frame containing new weighted values
data_transposed = data.T #changes from row to column format
data_transposed.columns = ['0_points', '10_points', '100_points', '1000_points', 'sub1000minus100', 'sub1000minus10', 'sub1000minus0', 'sub100minus10', 'sub100minus0', 'sub10minus0'] #adds a label to each column



data_transposed.to_excel("S3_JORT_ReactionTime_points.xlsx") #saves data into an excel form


