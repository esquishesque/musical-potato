import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys
import math

#full data frame with all data 
df=pd.read_excel('first survey - English final (Responses).xlsx',sheetname=5,skiprows=1,keep_default_na=False)
#df=pd.read_excel('survey_test.xls',sheetname=1)

#get the column names 
c=df.columns

#select the subset of the questions that are about wages etc
cdep=70
cdiv=71
ccampus=72
cexp=77
cage=78

wagesStart = 2
hiringStart = 7
workloadStart = 14
leavesStart = 21
workcondStart = 24
trainingStart = 29
equityStart = 34
interactionStart = 41
healthStart = 45
financeStart = 49
fundingStart = 55

wagesLen = 5
hiringLen = 7
workloadLen = 7
leavesLen = 3
workcondLen = 5
trainingLen = 5
equityLen = 7
interactionLen = 4
healthLen = 4
financeLen = 6
fundingLen = 3

cwages=c[wagesStart:wagesStart+wagesLen]
chiring=c[hiringStart:hiringStart+hiringLen]
cworkload=c[workloadStart:workloadStart+workloadLen]
cleaves=c[leavesStart:leavesStart+leavesLen]
cworkcond=c[workcondStart:workcondStart+workcondLen]
ctraining=c[trainingStart:trainingStart+trainingLen]
cequity=c[equityStart:equityStart+equityLen]
cinteraction=c[interactionStart:interactionStart+interactionLen]
chealth=c[healthStart:healthStart+healthLen]
cfinance=c[financeStart:financeStart+financeLen]
cfunding=c[fundingStart:fundingStart+fundingLen]



#set up other variables
issues_list=[cwages,chiring,cworkload,cleaves,cworkcond,ctraining,cequity,cinteraction,chealth,cfinance,cfunding]
titles_list = [issue[0][:issue[0].find(" [")] for issue in issues_list]
#this is a hack, but the slash in one entry is a problem
titles_list[-2].replace('/','-')
numResponses = len(df.index)

#clean up df and set up binaries for affects and imporant
binariesStart = len(c)
binaries_issues_list=[]
issuesColNames = c[wagesStart:fundingLen+fundingStart]

for issue in issues_list:
    start = len(df.columns)
    for question in issue: #using contains because there are a few variations on the exact wording
        df[question][(df[question].str.contains("UofT")==True)]="important"
        df[question][(df[question].str.contains("both")==True)]="both"
        df[question][(df[question].str.contains("personally")==True)]="affects"
        df[question][(df[question].str.contains("N/A")==True)]="neither"


        #set up columns for affects and important binaries
        temp1 = question + " - affects"
        temp2 = question + " - important"
        df[temp1] = ((df[question] == "affects") | (df[question] == "both"))
        df[temp2] = ((df[question] == "important") | (df[question] == "both"))
        df[temp1].replace(True,"affects",inplace=True)
        df[temp2].replace(True,"important",inplace=True)

    #creates a list of tuples with the start loc and num rows for each issue
    binaries_issues_list.append((start,len(df.columns)-start))


##################################################

script_option=int(sys.argv[1])

#for debugging
if script_option==0:
    pass

if script_option==1:
#loop over the issues_list
    for ii in range(0,len(issues_list)):
        #clear the figure if one previous 
        plt.clf()
        #define a figure with a size because we want to save it now
        f=plt.figure(figsize=(10,12),dpi=100)
        f.suptitle(titles_list[ii])
        #loop over every item in each sub category 
        for jj in range(0,len(issues_list[ii])):
            #set the subplot axes
            plt.subplot(len(issues_list[ii]),1,jj+1)
            #plot the histogram, sort_index sets the items alphabetically
            df[issues_list[ii][jj]].value_counts().sort_index().plot.barh()
            #set the xaxis based on the total number of responses
            plt.xlim([0,numResponses])
            #add a title so we remember what it is
            plt.title(issues_list[ii][jj][(issues_list[ii][jj].find("[")+1):len(issues_list[ii][jj])-1])
            #add some blank space
            f.subplots_adjust(hspace=1)
        #outputs the figures 
        f.savefig(titles_list[ii].replace("/",".")+'_hist.png')

if script_option==3:
    #analysis just of binary affects/important questions
    for ii in range(0,len(binaries_issues_list)):
        #clear the figure if one previous
        plt.clf()
        #define a figure with a size because we want to save it now
        f=plt.figure(figsize=(10,12),dpi=100)
        f.suptitle(titles_list[ii])
        #loop over every item in each sub category
        for jj in range(binaries_issues_list[ii][1]):
            currentCol = binaries_issues_list[ii][0]+jj
            #set the subplot axes
            plt.subplot((math.ceil(binaries_issues_list[ii][1]/2)),2,jj+1)
            #plot the histogram, sort_index sets the items alphabetically
            df.iloc[:,currentCol][df.iloc[:,currentCol]!=False].value_counts().sort_index().plot.barh()
            #set the xaxis based on the total number of responses
            #plt.xlim([0,df[issues_list[ii][jj]].value_counts().sum()])
            plt.xlim([0,numResponses])
            #hackily title only every other one
            if(jj % 2 == 0):
                plt.title(df.columns[currentCol][(df.columns[currentCol].find("[")+1):(df.columns[currentCol].find("]"))], x=1)
            #add some blank space
            f.subplots_adjust(hspace=1)
        #outputs the figures
        f.savefig(titles_list[ii].replace("/",".")+'_binaries_hist.png')


if script_option==2:
    #Gender analysis section
    #I'm using a three category classification now, but I could do other things

    #this part is going to be a bit hacky because I don't want to assign new axes labels 
    #add a separate column to keep track of the new category
    df['G']='N'
    df['G'][df['Gender identity']=='Man']='M'
    df['G'][df['Gender identity']=='Cis, Man']='M'
    df['G'][df['Gender identity']=='Woman']='F'
    df['G'][df['Gender identity']=='Cis, Woman']='F'
    
    for ii in range(0,len(issues_list)):
             #clear the figure if one previous 
        plt.clf()
        #define a figure with a size because we want to save it now
        f=plt.figure(figsize=(15,30),dpi=100)
        #loop over every item in each sub category 
        for jj in range(0,len(issues_list[ii])):
            #set the subplot axes - subplot(nrows, ncols, plot_number)
            plt.subplot(len(issues_list[ii]),1,jj+1)
            #plot the histograme, sort_index sets the items alphabetically
            df2=df.groupby(df['G'])
            df2[issues_list[ii][jj]].value_counts().sort_index().plot.barh()
            #set the xaxis based on the total number of responses
            plt.xlim([0,df2[issues_list[ii][jj]].value_counts().sum()])
            #add a title so we remember what it is 
            plt.title(issues_list[ii][jj])
        #add some blank space 
        f.subplots_adjust(hspace=.5)
        #outputs the figures 
        f.savefig('Gender_'+titles_list[ii].replace("/",".")+'_hist.png')


def supercount_equity(df,Icol,col):
    Ei=df.loc[(df[Icol]=='yes') & ((df[col]=='important')| (df[col]=='both'))].count()[0]
    Ea=df.loc[(df[Icol]=='yes') & ((df[col]=='affects')| (df[col]=='both'))].count()[0]
    Ni=df.loc[(df[Icol]!='yes') & ((df[col]=='important')| (df[col]=='both'))].count()[0]
    Na=df.loc[(df[Icol]!='yes') & ((df[col]=='affects')| (df[col]=='both'))].count()[0]
    Es=df.loc[(df[Icol]=='yes')].count()[0]
    Ns=df.loc[(df[Icol]!='yes')].count()[0]
    return[float(Ei)/Es,float(Ea)/Es,float(Ni)/Ns,float(Na)/Ns]

def make_comp_plot_equity(df,Icol,cols,outname):
    counts=np.zeros([len(cols),4])
    for ii in range(0,len(cols)):
        counts[ii]=supercount_equity(df,Icol,cols[ii])
    counts*=100
    fig,ax=plt.subplots()
    fig.set_size_inches(24.5, 10.5)    
    ax.plot(counts[:,2],counts[:,3],'ro')
    for i, txt in enumerate(cols):
        ax.annotate(i, (counts[i,0],counts[i,1]))
        ax.plot(counts[i,0],counts[i,1],'bo',label=str(i)+'--- E : '+cols[i][cols[i].find("[")+1:-1])
        ax.annotate(i, (counts[i,2],counts[i,3]))
        ax.plot(counts[i,2],counts [i,3],'ro',label=str(i)+'--- N : '+cols[i][cols[i].find("[")+1:-1])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel('Affects (%)')
    plt.xlabel('Important (%)')
#    plt.tight_layout()
    fig.savefig(outname)

if script_option==4:
    eq_cols=['eq_race','eq_trans','eq_gender','eq_disability','eq_sexuality']
    for eq in eq_cols:
        for issues in issues_list:
            make_comp_plot_equity(df,eq,issues,'comp_plot_'+eq+'_'+issues[0][:issues[0].find("[")-1].replace('/','-')+'.png')
            
def supercount_work(df,Icol,col):
    TAs=float(df.loc[(df[Icol].str.contains('TA')==True)].count()[0])
    TAi=df.loc[(df[Icol].str.contains('TA')==True) & ((df[col]=='important')| (df[col]=='both')) ].count()[0]/TAs
    TAa=df.loc[(df[Icol].str.contains('TA')==True)  & ((df[col]=='affects')| (df[col]=='both'))].count()[0]/TAs

    CIs=float(df.loc[(df[Icol].str.contains('CI')==True)].count()[0])
    CIi=df.loc[(df[Icol].str.contains('CI')==True) & ((df[col]=='important')| (df[col]=='both')) ].count()[0]/CIs
    CIa=df.loc[(df[Icol].str.contains('CI')==True)  & ((df[col]=='affects')| (df[col]=='both'))].count()[0]/CIs

    CPOs=float(df.loc[(df[Icol].str.contains('CPO')==True)].count()[0])
    CPOi=df.loc[(df[Icol].str.contains('CPO')==True) & ((df[col]=='important')| (df[col]=='both')) ].count()[0]/CPOs
    CPOa=df.loc[(df[Icol].str.contains('CPO')==True)  & ((df[col]=='affects')| (df[col]=='both'))].count()[0]/CPOs

    AIs=float(df.loc[(df[Icol].str.contains('AI')==True)].count()[0])
    if AIs!=0:
        AIi=df.loc[(df[Icol].str.contains('AI')==True) & ((df[col]=='important')| (df[col]=='both')) ].count()[0]/AIs
        AIa=df.loc[(df[Icol].str.contains('AI')==True)  & ((df[col]=='affects')| (df[col]=='both'))].count()[0]/AIs
    else:
        AIi=0
        AIa=0
        
    return[TAi,TAa,CIi,CIa,CPOi,CPOa,AIi,AIa]

def make_comp_plot_work(df,cols,outname):
    counts=np.zeros([len(cols),8])
    for ii in range(0,len(cols)):
        counts[ii]=supercount_work(df,'What kind(s) of Unit 1 work have you done? ',cols[ii])
    counts*=100
    fig,ax=plt.subplots()
    fig.set_size_inches(24.5, 10.5)    
    ax.plot(counts[:,2],counts[:,3],'ro')
    for i, txt in enumerate(cols):
        ax.annotate(i, (counts[i,0],counts[i,1]))
        ax.plot(counts[i,0],counts[i,1],'bo',label=str(i)+'--- TA : '+cols[i][cols[i].find("[")+1:-1])
        ax.annotate(i, (counts[i,2],counts[i,3]))
        ax.plot(counts[i,2],counts [i,3],'ro',label=str(i)+'--- CI : '+cols[i][cols[i].find("[")+1:-1])
        ax.annotate(i, (counts[i,4],counts[i,5]))
        ax.plot(counts[i,4],counts[i,5],'go',label=str(i)+'--- CPO : '+cols[i][cols[i].find("[")+1:-1])
        ax.annotate(i, (counts[i,6],counts[i,7]))
        ax.plot(counts[i,6],counts [i,7],'mo',label=str(i)+'--- AI : '+cols[i][cols[i].find("[")+1:-1])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel('Affects (%)')
    plt.xlabel('Important (%)')
#    plt.tight_layout()
    fig.savefig(outname)

if script_option==5:
    for issues in issues_list:
        make_comp_plot_work(df,issues,'comp_plot_work_type_'+issues[0][:issues[0].find("[")-1].replace('/','-')+'.png')

def supercount_div(df,Icol,col):
    D1s=float(df.loc[(df[Icol].str.contains('Humanities')==True)].count()[0])
    D1i=df.loc[(df[Icol].str.contains('Humanities')==True) & ((df[col]=='important')| (df[col]=='both')) ].count()[0]/D1s
    D1a=df.loc[(df[Icol].str.contains('Humanities')==True)  & ((df[col]=='affects')| (df[col]=='both'))].count()[0]/D1s

    D2s=float(df.loc[(df[Icol].str.contains('Social')==True)].count()[0])
    D2i=df.loc[(df[Icol].str.contains('Social')==True) & ((df[col]=='important')| (df[col]=='both')) ].count()[0]/D2s
    D2a=df.loc[(df[Icol].str.contains('Social')==True)  & ((df[col]=='affects')| (df[col]=='both'))].count()[0]/D2s

    D3s=float(df.loc[(df[Icol].str.contains('Physical')==True)].count()[0])
    D3i=df.loc[(df[Icol].str.contains('Physical')==True) & ((df[col]=='important')| (df[col]=='both')) ].count()[0]/D3s
    D3a=df.loc[(df[Icol].str.contains('Physical')==True)  & ((df[col]=='affects')| (df[col]=='both'))].count()[0]/D3s

    D4s=float(df.loc[(df[Icol].str.contains('Life')==True)].count()[0])
    D4i=df.loc[(df[Icol].str.contains('Life')==True) & ((df[col]=='important')| (df[col]=='both')) ].count()[0]/D4s
    D4a=df.loc[(df[Icol].str.contains('Life')==True)  & ((df[col]=='affects')| (df[col]=='both'))].count()[0]/D4s

    D5s=float(df.loc[(df[Icol].str.contains('OISE')==True)].count()[0])
    D5i=df.loc[(df[Icol].str.contains('OISE')==True) & ((df[col]=='important')| (df[col]=='both')) ].count()[0]/D5s
    D5a=df.loc[(df[Icol].str.contains('OISE')==True)  & ((df[col]=='affects')| (df[col]=='both'))].count()[0]/D5s
        
    return[D1s,D1a,D2s,D2a,D3s,D3a,D4a,D4a,D5a,D5s]

def make_comp_plot_div(df,cols,outname):
    counts=np.zeros([len(cols),8])
    for ii in range(0,len(cols)):
        counts[ii]=supercount_work(df,'What department(s) are you a student in?',cols[ii])
    counts*=100
    fig,ax=plt.subplots()
    fig.set_size_inches(24.5, 10.5)    
    ax.plot(counts[:,2],counts[:,3],'ro')
    for i, txt in enumerate(cols):
        ax.annotate(i, (counts[i,0],counts[i,1]))
        ax.plot(counts[i,0],counts[i,1],'bo',label=str(i)+'--- D1 : '+cols[i][cols[i].find("[")+1:-1])
        ax.annotate(i, (counts[i,2],counts[i,3]))
        ax.plot(counts[i,2],counts [i,3],'ro',label=str(i)+'--- D2 : '+cols[i][cols[i].find("[")+1:-1])
        ax.annotate(i, (counts[i,4],counts[i,5]))
        ax.plot(counts[i,4],counts[i,5],'go',label=str(i)+'--- D3 : '+cols[i][cols[i].find("[")+1:-1])
        ax.annotate(i, (counts[i,6],counts[i,7]))
        ax.plot(counts[i,6],counts [i,7],'mo',label=str(i)+'--- D4 : '+cols[i][cols[i].find("[")+1:-1])
        ax.annotate(i, (counts[i,8],counts[i,9]))
        ax.plot(counts[i,8],counts [i,9],'mo',label=str(i)+'--- D5 : '+cols[i][cols[i].find("[")+1:-1])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel('Affects (%)')
    plt.xlabel('Important (%)')
#    plt.tight_layout()
    fig.savefig(outname)

if script_option==6:
    for issues in issues_list:
        make_comp_plot_work(df,issues,'comp_plot_student_div_'+issues[0][:issues[0].find("[")-1].replace('/','-')+'.png')

