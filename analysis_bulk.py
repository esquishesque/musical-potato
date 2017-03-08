import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#full data frame with all data 
df=pd.read_excel('first survey - final (Responses).xlsx',sheetname=1,skiprows=1,keep_default_na=False)
#df=pd.read_excel('survey_test.xls',sheetname=1)

#get the column names 
c=df.columns


#select the subset of the questions that are about wages
cwages=c[13:18]
chiring=c[18:25]
cworkload=c[25:32]
cleaves=c[32:35]
cworkcond=c[35:40]
ctraining=c[40:45]
cequity=c[45:52]
cinteraction=c[52:56]
chealth=c[56:60]
cfinance=c[60:66]
cfunding=c[66:69]
cdep=70
cdiv=71
ccampus=72
cexp=73
cage=74

issues_list=[cwages,chiring,cworkload,cleaves,cworkcond,ctraining,cequity,cinteraction,chealth,cfinance,cfunding]

#theres a better way to do this, but its too complicated for me to do right now 
titles_list=['wages','hiring','workload','leaves','workcond','training','equity','interactions','health','finance','funding']

#loop over the issues_list
for ii in range(0,len(issues_list)):
    #clear the figure if one previous 
    plt.clf()
    #define a figure with a size because we want to save it now
    f=plt.figure(figsize=(10,10),dpi=100)
    #loop over every item in each sub category 
    for jj in range(0,len(issues_list[ii])):
        #set the subplot axes
        plt.subplot(len(issues_list[ii]),1,jj+1)
        #change the indices so that they are a bit easier to read
        df[issues_list[ii][jj]][(df[issues_list[ii][jj]]=='This is important to me at UofT')]='important'
        df[issues_list[ii][jj]][(df[issues_list[ii][jj]]=='This is both important to me and affects me')]='important/affects'
        df[issues_list[ii][jj]][(df[issues_list[ii][jj]]=='This affects me personally')]='affects'
        df[issues_list[ii][jj]][(df[issues_list[ii][jj]]=='N/A')]='n/A'
        #plot the histograme, sort_index sets the items alphabetically 
        df[issues_list[ii][jj]].value_counts().sort_index().plot.barh()
        #set the xaxis based on the total number of responses
        plt.xlim([0,df[issues_list[ii][jj]].value_counts().sum()])
        #add a title so we remember what it is 
        plt.title(issues_list[ii][jj])
    #add some blank space 
    f.subplots_adjust(hspace=0.5)
    #outputs the figures 
    f.savefig(titles_list[ii]+'_hist.png')



