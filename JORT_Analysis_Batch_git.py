#Data Analysis_JORT_Pilot Study 2 (NEW OUTPUTS)

import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import os 

os.chdir("C://Users/cs16436/OneDrive - University of Bristol/Study4_MDDMINI/S4_Data/S4_JORT//")
#("D://Back-ups/Python Scripts//")
class Trial: #Defining what a trial is composed of 
    
    def __init__(self,error_file,participant,trial_number,forces,times,start_time,end_time,effort,condition,number,max_force,stimulus_index,graphs=False): #function - trial composed forces, start time, end time and trial number
        self.participant=participant
        self.trial_number=trial_number
        self.forces=forces
        self.relative_forces=[force/max_force for force in self.forces]
        self.start_time=start_time
        self.end_time=end_time
        self.condition=condition
        self.number=number
        self.total_time=float(end_time-start_time)
        self.stimulus_index=stimulus_index
        self.times=times        
        #self.force_start=0
        #self.force_end=0
        self.force_start=stimulus_index
        self.force_end=stimulus_index
        self.effort=effort
        
        
        self.find_force_start()
        self.find_force_end()        
        self.find_reaction_time()
        
        self.ignored=False
        
        if self.force_start==len(self.times):
            self.ignored=True
        if self.reaction_time<0:
       # if self.reaction_time==0:
            self.ignored=True
       
       
        
        #print self.start_time,self.condition,self.stimulus_index
        #plt.plot(self.forces)
        if graphs:
            plt.plot(self.forces)
            plt.axvline(self.force_start,color='b')
            plt.axvline(self.stimulus_index,color='g')
            plt.axvline(self.force_end,color='r')
            plt.show()
            


    def find_reaction_time(self):
        #start_stim_force=self.forces[self.stimulus_index]
        if len(self.times)!=0:
            if self.stimulus_index>len(self.times):
                error_file.write("f/p no stimulus in trial "+str(self.participant)+" "+str(self.trial_number)+"\n")
                self.reaction_time=-2
            else:
                if self.force_start==len(self.times):
                   self.reaction_time=-1  
                else:
                   self.reaction_time=self.times[self.force_start]-self.times[self.stimulus_index] #self.force_start
                  # self.reaction_time=self.times[start_stim_force]-self.times[self.stimulus_index]
                    
        # while self.relative_force_start(self.forces) < 2 if self.forces > 2
        #   self.

    def find_force_start(self): #finding start force
        start_stim_force=self.forces[self.stimulus_index]
       # while self.force_start<len(self.forces) and self.forces[self.force_start]<2:
        while self.force_start<len(self.forces) and self.forces[self.force_start]<start_stim_force+2:
                self.force_start+=1 
        
                
    def find_force_end(self): #finding force end 
        self.force_end=self.force_start+1
        
        while self.force_end<len(self.forces) and self.forces[self.force_end]>2:
            self.force_end+=1  
            
    def find_force_average(self):
        if self.force_end-self.force_start==1:
            return 0.0
        return np.mean(self.relative_forces[self.force_start:self.force_end])*100
    
    def find_velocity_start(self):
        self.velocity_start<len(self.velocity_approach) 
        self.velocity_start+=1
        
    def find_max_force(self):
        if len(self.relative_forces[self.force_start:self.force_end]):
            return np.max(self.relative_forces[self.force_start:self.force_end])*100                 
        else:
            return 0
    
        
   # def find_time_spent(self):
    #    if self.force_end - self.force_start==1:
     #       return 0.0
      #  return [self.find_force_end - self.find_force_start]
        
class Experiment:        
    def __init__(self,file_name,error_file):
        data_file = open(file_name, "r") #opening up file
        lines = data_file.readlines() #reading the file
        data_file.close() #closing the file        
        self.meta_data=lines.pop(0) #removing the first line which doesn't contain data
        self.participant=lines[0].split("\t") [0] #stating first column is participant, which is seperated by a tab
        self.max_force=float(lines[0].split("\t") [2]) #stating that max_force contains numbers which is 3rd column
        self.times=[float(line.split("\t") [1]) for line in lines] #2nd column (split by tab),data numbers 'defining line'
        self.forces=[float(line.split("\t")[6]) for line in lines] #7th column, (force)
        self.velocity=[float(line.split("\t") [7]) for line in lines] #8th column (velocity)
        self.velocity_avoid=[float(line.split("\t") [8]) for line in lines] #9th column velocity of red dot in avoid trials
        #self.velocity_approach=[float(line.split("\t") [9]) for line in lines] #10th column velocity of black dot in avoid trials AND velocity red dot in conflict trials
        self.velocity_approach=[float(line.split("\t") [11]) for line in lines] # WHEN STIMULUS APPEARS???
        #self.reaction_time=[float(line.split("\t") [9]) for line in lines]
        
        trial_numbers=[int(line.split("\t") [5]) for line in lines] #6th column (trial number)
        trial_types=[int(line.split("\t") [4]) for line in lines] #5th column trial type
        trial_efforts=[float(line.split("\t") [14]) for line in lines] #14th column effort ratio

                     
        trial_starts=[0] #trial starts at 0
        this_trial_number=trial_numbers[0]
        for i in range(1,len(trial_numbers)): #for each index in the list of all the times
            if trial_numbers[i]!=this_trial_number: #if trial no. is not equal to 0 
                trial_starts.append(i) #remember where new trials start
                this_trial_number=trial_numbers[i] #now checking new trial no. change
                
        trial_starts.append(len(trial_numbers)) #know where last trial ends

        self.trials=[] #Empty trials list
        
        #stimulus_starts=[0]
             
        for i in range(0,len(trial_starts)-1): #for each value in range 0 to length (-1 of next trial start) 
            stimulus_start=trial_starts[i]+2 #added change
            #while self.velocity_avoid[stimulus_start]+self.velocity_approach[stimulus_start]<0.5:
            while self.velocity_approach[stimulus_start] > 500:
                stimulus_start+=1
#            print (stimulus_start,self.velocity_approach[stimulus_start:stimulus_start+5])
            self.trials.append(
                    Trial(error_file,self.participant,trial_numbers[trial_starts[i]+1],
                        self.forces[trial_starts[i]:trial_starts[i+1]], #send relevant part forces vector to trial
                          self.times[trial_starts[i]:trial_starts[i+1]],
                          self.times[trial_starts[i]],
                          self.times[trial_starts[i+1]-1],
                            trial_efforts[trial_starts[i]],
                            trial_types[trial_starts[i]],
                            trial_numbers[trial_starts[i]],
                            #self.max_force,stimulus_start-2-trial_starts[i])
                            self.max_force,stimulus_start-trial_starts[i])
                    )


class Participant: #What a participant is
    def __init__(self,file_name): 
        self.experiment=Experiment(file_name)

def load_all_participants(participant_name_file): #load participant numbers from file
    participants=[] #participants variable is a list
    participant_file=open(participant_name_file,"r") #reading the file with participant numbers in
    participant_list=participant_file.readlines() #read lines in file
    for participant in participant_list:    
        participant=participant.rstrip('\n') # extract the number participants
        participants.append(participant) #file of participants
    return participants
    
#directory= os.chdir('\\ads.bris.ac.uk\filestore\MyFiles\StudentPG4\cs16436\Documents\PhD_SecondYear\Joystick Operated Runway Task (JORT)\Experiment2\\')
#participant_file_name="filenames.txt"

#participants=load_all_participants(directory,participant_file_name)

def make_zero(n):
    return [0 for _ in range(0,n)]


def output(out_files,participant,average_force_ec,max_forces_ec,not_dropped_ec,reaction_time_ec):
    for file in out_files:
        file.write(participant)
        file.write(",,,")
    for i in range(len(average_force_ec)):
        for j in range(len(average_force_ec[i])):
            out_files[0].write(str(average_force_ec[i][j]))
            out_files[1].write(str(max_forces_ec[i][j]))
            out_files[2].write(str(not_dropped_ec[i][j]))
            out_files[3].write(str(reaction_time_ec[i][j]))
            
            if j==len(average_force_ec[i])-1 and i==len(average_force_ec)-1:
                for file in out_files:
                    file.write("\n")
            else:   
                for file in out_files:
                    file.write(",")
                    
    
def make_out_files(file_name_root):
    out_files=[]
    file=open(file_name_root+"_av_force.csv","w") 
    out_files.append(file)
    file=open(file_name_root+"_max_force.csv","w") 
    out_files.append(file)    
    file=open(file_name_root+"_not_dropped.csv","w") 
    out_files.append(file)    
    file=open(file_name_root+"_rt.csv","w") 
    out_files.append(file)
    return out_files

out_file_name_root="jort_results_practice"

error_file=open("jort_errors.txt","w")

out_files=make_out_files(out_file_name_root)

participant_file_names=load_all_participants("participant_file_names.txt")

condition_n=11
tol=0.001
effort_values=[1.0,1.6,2.0,2.4]    
condition_values=[7,8,9,10]

for file_name in participant_file_names:

    experiment=Experiment(file_name,error_file)

    average_forces=make_zero(condition_n)
    not_dropped=make_zero(condition_n)
    start_time=make_zero(condition_n) #list values in each trial type
    end_time=make_zero(condition_n) 
    reaction_time=make_zero(condition_n)
    max_forces=make_zero(condition_n)
    force_c=0
 #force starts at 0
#conditions: 0,1, 4,6, 7-10

#def frange(start, stop, step):
 #   i = start
  #  while i < stop:
   #     yield i 
    #    i += step
 
       
    for condition in range (0,11): #for each different trial type
        force_c=0
        for trial in experiment.trials: # for each trial
            if trial.condition==condition: #if same conditions #if not trial.ignored and trial.condition
                average_forces[condition]+=trial.find_force_average() # append average forces for each same trial  
                start_time[condition]+=trial.force_start 
                end_time[condition]+=trial.force_end
                max_forces[condition]+=trial.find_max_force()
                force_c+=1
        not_dropped[condition]+=force_c
        if force_c!=0: #if force not equal to 0
            average_forces[condition]/=force_c #take average forces each condition
            start_time[condition]/=force_c
            end_time[condition]/=force_c
            max_forces[condition]/=force_c
            reaction_time[condition]/=force_c
        else:
            average_forces[condition]=0
            
            

#for i in range(len(average_forces)):
#print (i,average_forces[i],max_forces[i],not_dropped[i],reaction_time[i])
    


    average_force_ec=[[0.0 for _ in condition_values] for _ in effort_values]
    not_dropped_ec=[[0.0 for _ in condition_values] for _ in effort_values]
    start_time_ec=[[0.0 for _ in condition_values] for _ in effort_values]
    end_time_ec=[[0.0 for _ in condition_values] for _ in effort_values]
    max_forces_ec=[[0.0 for _ in condition_values] for _ in effort_values]
    reaction_time_ec=[[0.0 for _ in condition_values] for _ in effort_values]
    force_c_ec=0

    for effort_i,effort in enumerate(effort_values): #for each different trial type
        for condition_i,condition in enumerate(condition_values):
            force_c_ec=0
            rt_c_ec=0 #ADDED
            for trial in experiment.trials: # for each trial
                #if not trial.ignored and trial.condition==condition and abs(trial.effort-effort)<tol: #if same conditions 
                if trial.condition==condition and abs(trial.effort-effort)<tol:
                        average_force_ec[effort_i][condition_i]+=trial.find_force_average() # append average forces for each same trial  
                        start_time_ec[effort_i][condition_i]+=trial.force_start        
                        end_time_ec[effort_i][condition_i]+=trial.force_end
                        #if trial.reaction_time>0: #WAS >0
                         #   reaction_time_ec[effort_i][condition_i]+=trial.reaction_time #ADDED
                          #  rt_c_ec+=1 # ADDED                      
                        #if trial.reaction_time == 0:
                         #   np.replace.trial.reaction_time = -9999
                        max_forces_ec[effort_i][condition_i]+=trial.find_max_force()
                        force_c_ec+=1
                        if trial.reaction_time>0: #WAS >0
                            reaction_time_ec[effort_i][condition_i]+=trial.reaction_time #ADDED
                            rt_c_ec+=1 # ADDED 
            not_dropped_ec[effort_i][condition_i]+=force_c_ec
            if force_c_ec!=0: #if force not equal to 0
                average_force_ec[effort_i][condition_i]/=force_c_ec #take average forces each condition
                start_time_ec[effort_i][condition_i]/=force_c_ec
                end_time_ec[effort_i][condition_i]/=force_c_ec
                max_forces_ec[effort_i][condition_i]/=force_c_ec
               # reaction_time_ec[effort_i][condition_i]/=rt_c_ec
            else:
                average_force_ec[effort_i][condition_i]=0
            if rt_c_ec!=0:
                reaction_time_ec[effort_i][condition_i]/=rt_c_ec
    
    #np.where(trial.reaction_time==0,-9999,trial.reaction_time)

#    for i in range(len(average_force_ec)):
#        for j in range(len(average_force_ec[i])):
#            print (effort_values[i],condition_values[j],average_force_ec[i][j],max_forces_ec[i][j],not_dropped_ec[i][j],reaction_time_ec[i][j])
    print(experiment.participant)  
    output(out_files,experiment.participant,average_force_ec,max_forces_ec,not_dropped_ec,reaction_time_ec)



for file in out_files:
    file.close()
error_file.close()
    ##########################################

    
    
    