#INTRODUCTION:
#name: Dianne Guzman
#filename: finalproject.py (python file), subject100file.csv (data file)

#This experiment presents different images of inanimate objects. The participant must determine whether or not they see a face in the image.
#I made this experiment so I can analyze how people perceive inanimate objects and how it affects their reaction time.

#EXPERIMENT:

#modules
import psychopy
from psychopy import gui, visual, monitors, event, core
import os
import numpy as np
import pandas as pd
import csv

#experiment info dialogue box
exp_info = {'subject_nr':0, 'handedness':('right','left','ambi'), 
            'gender':('male','female','other','prefer not to say')}
            
my_dlg = gui.DlgFromDict(dictionary=exp_info)

filename = 'subject' + str(exp_info['subject_nr']) + 'file.csv'
print(filename)

#defining directories
os.chdir('/Applications/PsychoPy.app/Contents/Resources/psychopy')

main_dir = os.getcwd()
sub_dir = os.path.join(main_dir, 'sub_info', filename)
image_dir = os.path.join(main_dir,'fpimages')
path = os.path.join(main_dir, 'data')

#defining monitor and window
mon = monitors.Monitor('myMonitor', width=30.41, distance=60) 
mon.setSizePix([1440,900])
mon.save()
win = visual.Window(monitor=mon, size=(800,800), color=[-1,-1,-1])

#number of trials and blocks
nBlocks=2
nTrials=10
totalTrials = nTrials*nBlocks

#creating stimuli
stims = ['object01.jpg', 'object02.jpg', 'object03.jpg', 'object04.jpg', 'object05.jpg', 
            'object06.jpg', 'object07.jpg', 'object08.jpg', 'object09.jpg', 'object10.jpg']
start_msg = "Welcome to my experiment!"
instruct_msg = "You will be shown 3 images of inanimate objects for half a second. Press Y if you see a face. Press N if you don't"
question_msg = "Did you see a face? Y = yes, N = no"
end_msg = "End of experiment. Thank you!"

start_text = visual.TextStim(win, text=start_msg)
instruct_text = visual.TextStim(win, text=instruct_msg)
question_text = visual.TextStim(win, text=question_msg)
end_text = visual.TextStim(win, text=end_msg)
my_image = visual.ImageStim(win)

#create lists
keyList=['y','n']
blockNumber=[0]*totalTrials
trialNumber=[0]*totalTrials
respTime=[]
keys_pressed=[]

#creating clocks for response times
rt_clock = core.Clock()

#randomizing stimuli
np.random.shuffle(stims)

#present start and instruction messages before trial
start_text.draw()
win.flip()
event.waitKeys()

instruct_text.draw()
win.flip()
event.waitKeys()

#start block
for block in range(nBlocks):
    block_msg = "Block" + ' ' + str(block + 1)
    block_text = visual.TextStim(win, text=block_msg)
    
    block_text.draw()
    win.flip()
    event.waitKeys()
    
    #start trial
    for trial in range(nTrials):
        keys=event.getKeys(keyList=keyList)
        overallTrial = block*nTrials+trial
        blockNumber[overallTrial] = block+1
        trialNumber[overallTrial] = trial+1
        my_image.image = os.path.join(image_dir,stims[trial])
        rt_clock.reset()
    
        my_image.draw()
        win.flip()
        core.wait(.5)
        
        question_text.draw()
        win.flip()
        core.wait(3)
        
        if keys:
            react_time = rt_clock.getTime()
            respTime.append(react_time-3)
            keys_pressed.append(keys)
            
    print(respTime)
    print(keys_pressed)

#present end message
end_text.draw()
win.flip()
event.waitKeys()

#create data file
data = {"Block Number": blockNumber, "Trial Number": trialNumber, "Key pressed": keys_pressed,"Response Time": respTime}
df = pd.DataFrame.from_dict(data, orient='index')
df=df.transpose()

df.to_csv(os.path.join(path, filename), sep=',', index=False)

#close window
win.close()