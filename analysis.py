import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#full data frame with all data 
df=pd.read_excel('first survey - final (Responses).xlsx',sheetname=1,skiprows=1)
#df=pd.read_excel('survey_test.xls',sheetname=1)

#get the column names 
c=df.columns

#select the subset of the questions that are about wages
cwages=c[13:18]

#test to see the output for the value count function
a=df.groupby(c[1])
print(a)

#make a bar plot of all wage questions
f0=plt.figure(0)
for ii in range(0,len(cwages)):
    plt.subplot(len(cwages),1,ii+1)
    df[cwages[ii]].value_counts().plot.barh()
    plt.title(cwages[ii])
f0.subplots_adjust(hspace=0.5)

#make a bar plot of just the response from the humanities folks
f1=plt.figure(1)
for ii in range(0,len(cwages)):
    plt.subplot(len(cwages),1,ii+1)
    df.where(df['Which division(s) have you done Unit 1 work in?']=='Humanities')[cwages[ii]].value_counts().plot.barh()
    plt.title(cwages[ii])
f1.subplots_adjust(hspace=0.5)

plt.show()
    


