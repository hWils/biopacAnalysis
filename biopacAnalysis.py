# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:17:51 2019

@author: Holly
"""

# demo: http://uwmadison-chm.github.io/bioread/bioread_quick_demo.html

# http://pydoc.net/biosppy/0.5.1/biosppy.signals.ecg/
# filtering: https://python-heart-rate-analysis-toolkit.readthedocs.io/en/latest/_modules/heartpy/filtering.html


# also neurokit- but doesnt seem to be working properly

import neurokit as nk
import matplotlib.pyplot as plt
import bioread as bio #for reading biopac files

from biosppy import storage
from biosppy.signals import ecg
from biosppy.signals import eda
import heartpy as hp
import numpy as np


#pathOriginal = 'moodData/3_fear.acq'
#pathConvTxt = 'dataCSVed.txt'


# SO FAR: code takes in two separate acq files for mood and baseline, filters using biosppy and returns the BPM for both conditions
# WORKING ON: what needs to be returned for eda

dataBaseline = bio.read_file('moodData/ak_scary_baseline.acq')
dataMood = bio.read_file('moodData/ak_scary_mood.acq')
print(dataBaseline.channels)

for chan in dataBaseline.channels:
    #if chan.name == 'ECG (.05 - 150 Hz)':
    if chan.name == 'Pulse':
      #  plt.plot(chan.time_index, chan.data, label='{} ({})'.format(chan.name, chan.units))
        print(type(chan.data))
        ecg_BPM_baseline = chan.data
    if chan.name =='EDA (0 - 35 Hz)':
        EDA_baseline= chan.data
        
for chan in dataMood.channels:
   # if chan.name == 'ECG (.05 - 150 Hz)':
    if chan.name == 'Pulse':
     #   plt.plot(chan.time_index, chan.data, label='{} ({})'.format(chan.name, chan.units))
        print(type(chan.data))
        ecg_BPM_mood = chan.data
    if chan.name =='EDA (0 - 35 Hz)':
        EDA_mood= chan.data
        

outecgBaseline = ecg.ecg(signal=ecg_BPM_baseline, sampling_rate=200., show=True)
heart_rate_base = outecgBaseline[6]
BPM_base = heart_rate_base.mean()
outecgMood = ecg.ecg(signal=ecg_BPM_mood, sampling_rate=200., show=True)
heart_rate_mood = outecgMood[6]
BPMm = heart_rate_mood.mean()
print(BPM_base, " : ", BPMm)

outEDABaseline = eda.eda(signal=EDA_baseline, sampling_rate=200., show=True)
outEDAMood = eda.eda(signal=EDA_mood, sampling_rate=200., show=True)
print(outEDABaseline[3])

plt.plot(list(range(len(EDA_baseline))),EDA_baseline, color = 'blue')
plt.plot(list(range(len(EDA_mood))),EDA_mood, color = 'red')




# convert acqKnowedge file to MATLAB file or to Text file if neded, but looks liek analysis should be possible in python
"""
# (1) load in the file as a df using neurokit
df, sampling_rate = nk.read_acqknowledge(pathOriginal, return_sampling_rate=True)
print(sampling_rate)
# (2) split the data into the channels; here I have retrieved the ECG channel
data = df["ECG (.05 - 150 Hz)"] #series
# (3) convert the df into a csv file so it can be read by the hp package
dataAsCv = data.to_csv(pathConvTxt)
# (4) adds headings of 'time' and 'hr' to txt file - necerssary for hp package
with open(pathConvTxt, 'r') as original: origData = original.read()
with open(pathConvTxt, 'w') as modified: modified.write("time,hr\n" + origData)

# (5) get datetime data and hr data separately
datetime_data = hp.get_data(pathConvTxt, column_name = 'time')
hr_data = hp.get_data(pathConvTxt, column_name = 'hr')

# (6) check the samplerate is as expected, should be 2000Hz
fs = hp.get_samplerate_datetime(datetime_data, timeformat='%Y-%m-%d %H:%M:%S.%f')
print(fs)
"""

# next step is to extract based on baseline vs. mood   - need biopac library for this
"""
# (1) load in file
data1 = bio.read_file(pathOriginal) #biopac datafile
# (2) extract index for event markers so can be split into baseline and mood
baseline = [0,0]
mood = [0,0]
for m in data1.event_markers:
    if "beginBaseline" in m.text:
        baseline[0] = m.sample_index
    if "finishBaseline" in m.text:
        baseline[1] = m.sample_index
    if "beginMood" in m.text:
        mood[0] = m.sample_index
    if "endMood" in m.text:
        mood[1] = m.sample_index
        
    if len(m.text) > 1:
        print('{0}: Channel {1}, type {2}'.format(m.text, m.channel_name, m.type))
        print(m.sample_index)
        
baselineData = hr_data[baseline[0]:baseline[1]]
moodData = hr_data[mood[0]:mood[1]]
        
#baselineData = hp.enhance_peaks(baselineData)
#moodData = hp.enhance_peaks(moodData)
# (7) filter the signal to be in a particular range otherwise it will not be possible to plot
# "return_top flag to only return the filter response that has amplitute above zero. We’re only interested in the peaks, and sometimes this can improve peak prediction:"
filteredBaseline = hp.filter_signal(baselineData, cutoff = [0.75, 3.5], sample_rate = 200.0, order = 3, filtertype='bandpass',return_top = True)
filteredMood = hp.filter_signal(moodData, cutoff = [0.75, 3.5], sample_rate = 200.0, order = 3, filtertype='bandpass',return_top = True)
#filteredBaseline = hp.filter_signal(filteredBaseline, cutoff = 0.05, sample_rate = 2000.0, filtertype='notch')
#filteredMood = hp.filter_signal(filteredMood, cutoff = 0.05, sample_rate = 2000.0, filtertype='notch')


       
        
# (8) print out the plotted data
working_data, measures = hp.process(filteredMood, 200.0)
print(measures['bpm'])
hp.plotter(working_data, measures, moving_average = True)

#working_data, measures = hp.process_segmentwise(filteredMood, sample_rate=2000.0,  segment_width = 40, segment_overlap = 0.25, calc_freq=True, reject_segmentwise=True, report_time=True)
#hp.plotter(working_data, measures)

"""
        
        
# manually print this index into console


#df, sampling_rate = nk.read_acqknowledge('moodData/holly_baseline_segment.acq', return_sampling_rate=True)
# (1) load in file

#heart_rate_base = outEDABaseline[6]

########################   https://python-heart-rate-analysis-toolkit.readthedocs.io/en/latest/heartrateanalysis.html



#baselineData = data1.channels[0].data[10820:370330]
#moodData = data1.channels[0].data[1486730:1911010]

#filtered = hp.filter_signal(baselineData, cutoff = 15, sample_rate = 2000.0, order = 1, filtertype='lowpass')
#filtered = hp.filter_signal(filtered, cutoff = 0.75, sample_rate = 2000.0, order = 3, filtertype='highpass')


#working_data, measures = hp.process(baselineData, 100.0,calc_freq=True)
#hp.plotter(working_data, measures)




   # print("M ;", m.__dict__)

"""



working_data, measures = hp.process(data, 100.0)
hp.plotter(working_data, measures)




"""

"""

#working_data, measures = hp.process_segmentwise(data, sample_rate=100.0, segment_width = 40, segment_overlap = 0.25)

#out = ecg.ecg(signal=df["ECG (.05 - 150 Hz)"], sampling_rate=1000., show=True)
#indces = ecg.christov_segmenter(signal=df["ECG (.05 - 150 Hz)"], sampling_rate=1000)
#hb = ecg.extract_heartbeats(signal=df["ECG (.05 - 150 Hz)"], rpeaks=indces, sampling_rate=1000,before=0.2, after=0.4)

## some automatic processing
#bioDf = nk.bio_process(ecgdf=df["ECG (.05 - 150 Hz)"], edadf=df["EDA (0 - 35 Hz)"], sampling_rate = 100)
#

#print(bioDf)
#bioDf.plot()



#bioDf["ECG"]["Average_Signal_Quality"]
#pd.DataFrame(bio["ECG"]["Cardiac_Cycles"]).plot(legend=False)  # Plot all the heart beats

# how to return event triggers from this
# is there a column in the df for this - .05-150hz;  0-35Hz; 
# what are these used for; 



data1 = bio.read_file('practice1.acq')
data2 = bio.read_file('practice2.acq')

data1
data2

data1.channels

EDA_data = copy.deepcopy(data1)
ECG_data = []
EDA_data_baseline = []
ECG_data_baseline = []



plt.subplot(211)

# split the two channels

for chan in data1.channels:
    if chan.name == 'ECG (.05 - 150 Hz)':
        plt.plot(chan.time_index, chan.data, label='{} ({})'.format(chan.name, chan.units))
   # if chan.name == 'ECG (.05 - 150 Hz)':
    #    EDA_data = chan
     #   print('This is ECG data')
     
     
        


#"soccer" in str


     #   ECG_data_baseline = 
    
print(type(data1.channels[0].data));

plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=1, mode="expand", borderaxespad=0.)
None  # Don't print a silly legend thing



"""

  #  print(type(m))
    
"""       
# (8) print out the plotted data
filteredBPM_mood = hp.filter_signal(ecg_BPM_mood, cutoff = [0.75, 3.5], sample_rate = 200.0, order = 3, filtertype='bandpass',return_top = True)
#filteredBPM_mood = hp.enhance_peaks(filteredBPM_mood)
working_data, measures = hp.process(filteredBPM_mood, 200.0)

hp.plotter(working_data, measures)
        
print(ecg_BPM_baseline.mean())   
print(ecg_BPM_mood.mean())  

#filteredBPM_mood = hp.enhance_ecg_peaks(hp.scale_data(filteredBPM_mood), 200, 
                               # aggregation='median', iterations=5)

"""
#wd, m = hp.process(hp.scale_data(filteredBPM_mood[900:2000]), 200)   
#plt.figure(figsize=(13,4))
#hp.plotter(wd, m)
        

#signal, mdata = storage.load_txt(pathConvTxt)
# process it and plot