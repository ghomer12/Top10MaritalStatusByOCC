#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:08:55 2020

@author: greerhomer
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt

#show all columns
pd.set_option('display.max_columns', None)

#load census occupation code by 1950 basis data 
codeReference=pd.read_csv('OCC1950_codes.txt', sep='\t', header = None)
codeReference = codeReference.rename(columns={0: "OCC1950", 1: "Profession"})

#load census data from ipums
data = pd.read_csv('usa_00004.csv')
data.shape #(123922411, 4)
data.head(5)

#drop all rows that have null values
df = data.dropna()
df.head(10)
df.shape #(123067661, 4)

#get counts per category by year
grouped_df = df.groupby(['YEAR', 'MARST', 'OCC1950' ]).size().reset_index(name='counts')
grouped_df.shape #(35762, 4)
grouped_df.head(10)

#looking into national information
grouped_df['OCC1950'].nunique()
nationalOCCList = grouped_df['OCC1950'].unique()

#Look at marital rates by female lead professions by marital type
def maritalRatesALL(grouped_df, codes):
    grouped_df = grouped_df[grouped_df.OCC1950.isin(codes)].reset_index()
    groupedDF = grouped_df.groupby(['YEAR', 'MARST'])['counts'].sum().reset_index(name='mariageStatusCount')
    teacherPop = groupedDF.groupby(['YEAR'])['mariageStatusCount'].sum().reset_index(name='Count')
    df2 = groupedDF.merge(teacherPop, on='YEAR', how='inner')
    df2['percent'] = df2['mariageStatusCount']/df2['Count']*100
    df2['MaritalStatus'] = 0
    for i in range(df2.shape[0]):
        if df2['MARST'][i] ==1:
            df2['MaritalStatus'][i] = 'Married, spouse present'
        elif df2['MARST'][i] == 2:
            df2['MaritalStatus'][i] = 'Married, spouse absent'
        elif df2['MARST'][i] == 3:
            df2['MaritalStatus'][i] = 'Separated'
        elif df2['MARST'][i] == 4:
            df2['MaritalStatus'][i] = 'Divorced'
        elif df2['MARST'][i] == 5:
            df2['MaritalStatus'][i] = 'Widowed'
        elif df2['MARST'][i] == 6:
            df2['MaritalStatus'][i] = 'Never married/single'
    df3 = df2.groupby(['YEAR', "MaritalStatus"])['percent'].sum().reset_index(name='percent')
    if len(codes) == 1:
        titleCode = codes[0]
        for i in range(len(codeReference['OCC1950'])):
            if codeReference['OCC1950'][i] == titleCode:
                title = codeReference['Profession'][i]
                sns.lineplot(data=df3, x='YEAR', y="percent", hue="MaritalStatus").set_title(title)
    else:
        sns.lineplot(data=df3, x='YEAR', y="percent", hue="MaritalStatus")

    return(df3)

#looking at different known female-dominated work forces
national = maritalRatesALL(grouped_df, nationalOCCList) #national
vets = maritalRatesALL(grouped_df, [98]) #vets
naturalScienceProfessorsInstructors = maritalRatesALL(grouped_df, [26]) #natural sciences
naturalScientists = maritalRatesALL(grouped_df, [69]) #natural sciences
Pharmacists = maritalRatesALL(grouped_df, [73]) #Pharmacists
Teachers = maritalRatesALL(grouped_df, [93]) #Pharmacists

#(something my mom was interested in)
accountants = maritalRatesALL(grouped_df, [000]) #Accountants

#Look at marital rates by female lead professions by combining the various 
#married types into one married category
def maritalRates(grouped_df, codes):
    grouped_df = grouped_df[grouped_df.OCC1950.isin(codes)].reset_index()
    groupedDF = grouped_df.groupby(['YEAR', 'MARST'])['counts'].sum().reset_index(name='mariageStatusCount')
    teacherPop = groupedDF.groupby(['YEAR'])['mariageStatusCount'].sum().reset_index(name='Count')
    df2 = groupedDF.merge(teacherPop, on='YEAR', how='inner')
    df2['percent'] = df2['mariageStatusCount']/df2['Count']*100
    df2['MaritalStatus'] = 0
    for i in range(df2.shape[0]):
        if df2['MARST'][i] < 4:
            df2['MaritalStatus'][i] = 'Married'
        elif df2['MARST'][i] == 4:
            df2['MaritalStatus'][i] = 'Divorced'
        elif df2['MARST'][i] == 5:
            df2['MaritalStatus'][i] = 'Widowed'
        elif df2['MARST'][i] == 6:
            df2['MaritalStatus'][i] = 'Single, Never Married'
    df3 = df2.groupby(['YEAR', "MaritalStatus"])['percent'].sum().reset_index(name='percent')
    if len(codes) == 1:
        titleCode = codes[0]
        for i in range(len(codeReference['OCC1950'])):
            if codeReference['OCC1950'][i] == titleCode:
                title = codeReference['Profession'][i]
                sns.lineplot(data=df3, x='YEAR', y="percent", hue="MaritalStatus").set_title(title)
    else:
        sns.lineplot(data=df3, x='YEAR', y="percent", hue="MaritalStatus")

    return(df3)

#looking at different known female-dominated work forces
national1 = maritalRates(grouped_df, nationalOCCList) #national
vets1 = maritalRates(grouped_df, [98]) #vets
naturalScienceProfessorsInstructors1 = maritalRates(grouped_df, [26]) #natural sciences
naturalScientists1 = maritalRates(grouped_df, [69]) #natural sciences
Pharmacists1 = maritalRates(grouped_df, [73]) #Pharmacists
Teachers1 = maritalRates(grouped_df, [93]) #Pharmacists

#get  marital rates by profession for csv export:
def maritalRatesTotal(grouped_df):
    groupedDF = grouped_df.groupby(['YEAR', 'OCC1950', 'MARST'])['counts'].sum().reset_index(name='mariageStatusCount')
    teacherPop = groupedDF.groupby(['YEAR', 'OCC1950'])['mariageStatusCount'].sum().reset_index(name='Count')
    df2 = groupedDF.merge(teacherPop, on=['YEAR', 'OCC1950'], how='inner')
    df2['percent'] = df2['mariageStatusCount']/df2['Count']*100
    df2['MaritalStatus'] = 0
    for i in range(df2.shape[0]):
        if df2['MARST'][i] ==1:
            df2['MaritalStatus'][i] = 'Married, spouse present'
        elif df2['MARST'][i] == 2:
            df2['MaritalStatus'][i] = 'Married, spouse absent'
        elif df2['MARST'][i] == 3:
            df2['MaritalStatus'][i] = 'Separated'
        elif df2['MARST'][i] == 4:
            df2['MaritalStatus'][i] = 'Divorced'
        elif df2['MARST'][i] == 5:
            df2['MaritalStatus'][i] = 'Widowed'
        elif df2['MARST'][i] == 6:
            df2['MaritalStatus'][i] = 'Never married/single'
    #get names of each profession
    df3 = df2.merge(codeReference, on='OCC1950', how='inner')
    return(df3)

#export marriage rates by profession to csv
df_allData = maritalRatesTotal(grouped_df)
df_allData.to_csv(index=False)
df_allData.to_csv('MaritalRatesByProfession.csv', index=False)

#also export national rates to a separate csv
national.to_csv('NationalRates.csv', index=False)

#explore top professions 
MarriedSpouseAbsent = df_allData.loc[df_allData['MaritalStatus'] == 'Married, spouse absent']
years = df_allData['YEAR'].unique()
years = np.sort(years)

#function that returns the top 10 highest percentages in a certain category
def top10(df, MartialStatusString):
    years = df['YEAR'].unique()
    years = np.sort(years)
    maritalStatusOfInterest = df.loc[df['MaritalStatus'] == MartialStatusString]
    top10 = pd.DataFrame()
    for i in years:
        print('printing the year: ', i)
        df_top = maritalStatusOfInterest.loc[maritalStatusOfInterest['YEAR'] == i].sort_values(by='percent', ascending=False).reset_index()[:10]
        print(df_top['Profession'])
        values =  df_top['Profession'].values
        top10[i]= values
    return(top10)

mariedSpouseAbsent = top10(df_allData, 'Married, spouse absent')
Divorced = top10(df_allData, 'Divorced')
mariedSpousePresent = top10(df_allData, 'Married, spouse present')
Single = top10(df_allData, 'Never married/single')
Separated = top10(df_allData, 'Separated')
Widowed = top10(df_allData, 'Widowed')

years = years[11:] #only take 2000 to 2019 since that is when the data incriments by every one year
Widowed.shape
#get the counts of professions that make the top 10 in each marriage status category across the years
def getCounts(top10df):
    counts = {}
    for year in years:
        for index, row in top10df.iterrows():
            if row[year] not in counts.keys():
                counts[row[year]] = 1
            else:
                counts[row[year]] += 1
    counts = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}
    return counts
     
top10WidowedCounts = getCounts(Widowed)
top10DivorcedCounts = getCounts(Divorced)
top10mariedSpousePresentCounts = getCounts(mariedSpousePresent)
top10mariedSpouseAbsentCounts = getCounts(mariedSpouseAbsent)
top10SingleCounts = getCounts(Single)
top10SeparatedCounts = getCounts(Separated)


#Create a top 10 dataframe



def getTop10DF(MaritalStatus, top10):
    dataset = pd.DataFrame({'MaritalStatus': MaritalStatus, 'OCC': list(top10.keys()), 
                            'Count': list(top10.values())}, columns=['MaritalStatus', 'OCC', 'Count'])
    return dataset
a = getTop10DF('Widowed', top10WidowedCounts)
b = getTop10DF('Divorced', top10DivorcedCounts)
c = getTop10DF('Maried Spouse Present', top10mariedSpousePresentCounts)
d = getTop10DF('Maried Spouse Absent', top10mariedSpouseAbsentCounts)
e = getTop10DF('Single Never Maried', top10SingleCounts)
f = getTop10DF('Separated', top10SeparatedCounts)

e[:12]
a.shape[0] + b.shape[0]+c.shape[0]+d.shape[0]+e.shape[0]+f.shape[0]
#get dataframe with top 10 counts
top10DF = pd.DataFrame()
top10DF = top10DF.append(a[:12], ignore_index=True)
top10DF = top10DF.append(b[:12], ignore_index=True)
top10DF = top10DF.append(c[:12], ignore_index=True)
top10DF = top10DF.append(d[:12], ignore_index=True)
top10DF = top10DF.append(e[:12], ignore_index=True)
top10DF = top10DF.append(f[:12], ignore_index=True)

top10DF.shape

#dataset used for top 10 bar graph
top10DF.to_csv('top10Counts_2000_2019.csv', index=False)



#Build New Dictionary
allTop10Count = {}
allTop10Count['Widowed'] = top10WidowedCounts
allTop10Count['Divorced'] = top10DivorcedCounts
allTop10Count['Maried Spouse Present'] = top10mariedSpousePresentCounts
allTop10Count['Maried Spouse Absent'] = top10mariedSpouseAbsentCounts
allTop10Count['Single Never Maried'] = top10SingleCounts
allTop10Count['Separated'] = top10SeparatedCounts


maritalStatusOfInterest = df_allData.loc[df_allData['MaritalStatus'] == 'Separated']
top10= pd.DataFrame()

for i in years:
    print('printing the year: ', i)
    df_top = maritalStatusOfInterest.loc[maritalStatusOfInterest['YEAR'] == i].sort_values(by='percent', ascending=False).reset_index()[:10]
    print(df_top['Profession'])
    values =  df_top['Profession'].values
    top10[i]= values
    

top10_MarriedSpouseAbsent = pd.DataFrame()
for i in years:
    print('printing the year: ', i)
    SpouseAbsent = MarriedSpouseAbsent.loc[MarriedSpouseAbsent['YEAR'] == i].sort_values(by='percent', ascending=False).reset_index()[:10]
    print(SpouseAbsent['Profession'])
    values =  SpouseAbsent['Profession'].values
    top10_MarriedSpouseAbsent[i]= values
        #top10Married[:, p] = married['Profession']
        #print(married['Profession'])


#Curiosity: highest marriage rates by year... Group all married types together
df_allData.columns
#get  marital rates by profession for csv export:
def maritalRatesTotalGrouped(grouped_df):
    groupedDF = grouped_df.groupby(['YEAR', 'OCC1950', 'MARST'])['counts'].sum().reset_index(name='mariageStatusCount')
    teacherPop = groupedDF.groupby(['YEAR', 'OCC1950'])['mariageStatusCount'].sum().reset_index(name='Count')
    df2 = groupedDF.merge(teacherPop, on=['YEAR', 'OCC1950'], how='inner')
    df2['percent'] = df2['mariageStatusCount']/df2['Count']*100
    df2['MaritalStatus'] = 0
    for i in range(df2.shape[0]):
        if df2['MARST'][i] < 4:
            df2['MaritalStatus'][i] = 'Married'
        elif df2['MARST'][i] == 4:
            df2['MaritalStatus'][i] = 'Divorced'
        elif df2['MARST'][i] == 5:
            df2['MaritalStatus'][i] = 'Widowed'
        elif df2['MARST'][i] == 6:
            df2['MaritalStatus'][i] = 'Single, Never Married'
    #get names of each profession
    df3 = df2.groupby(['YEAR', "OCC1950", "MaritalStatus"])['percent'].sum().reset_index(name='percent')

    df3 = df3.merge(codeReference, on='OCC1950', how='inner')

    return(df3)



df_grouped = maritalRatesTotalGrouped(grouped_df)

df_Married = df_grouped.loc[df_grouped['MaritalStatus'] == 'Married']
df_Divorced = df_grouped.loc[df_grouped['MaritalStatus'] == 'Divorced']
df_Single = df_grouped.loc[df_grouped['MaritalStatus'] == 'Single']
df_Widowed = df_grouped.loc[df_grouped['MaritalStatus'] == 'Widowed']

df_Married.sort_values(by='percent', ascending=False)
#there is clearly some issues with earlier years here where only some data was available

df_Divorced = df_grouped.loc[df_grouped['MaritalStatus'] == 'Divorced']
df_Single = df_grouped.loc[df_grouped['MaritalStatus'] == 'Single']
df_Widowed = df_grouped.loc[df_grouped['MaritalStatus'] == 'Widowed']

years = df_grouped['YEAR'].unique()

top10Married = np.zeros((10,len(years)))
top10Divorced = np.zeros((11,len(years)))
top10Single = np.zeros((11,len(years)))
top10Widowed = np.zeros((11,len(years)))

top10Married = pd.DataFrame()

for i in years:
    married = df_Married.loc[df_Married['YEAR'] == i]
    for j in range(len(married)):
        married = married.sort_values(by='percent', ascending=False)[:10]
        for p in range(len(years)):
            top10Married[i] = married['Profession']
            top10Married[:, p] = married['Profession']
        #print(married['Profession'])

top10Married.shape

#married
top10Married = pd.DataFrame()
for i in years:
    print('printing the year: ', i)
    married = df_Married.loc[df_Married['YEAR'] == i].sort_values(by='percent', ascending=False).reset_index()[:10]
    print(married['Profession'])
    values =  married['Profession'].values
    top10Married[i]= values

top10Married = top10Married.reindex(sorted(top10Married.columns), axis=1)
top10Married.to_csv('top10Married.csv', index=False)

top10Married.values[0]

top10Divorced = pd.DataFrame()
for i in years:
    print('printing the year: ', i)
    divorced = df_Divorced.loc[df_Divorced['YEAR'] == i].sort_values(by='percent', ascending=False).reset_index()[:10]
    print(divorced['Profession'])
    values =  divorced['Profession'].values
    top10Divorced[i]= values

top10Divorced = top10Divorced.reindex(sorted(top10Divorced.columns), axis=1)

top10Divorced.values[0]

top10Widowed = pd.DataFrame()
for i in years:
    print('printing the year: ', i)
    Widowed = df_Widowed.loc[df_Widowed['YEAR'] == i].sort_values(by='percent', ascending=False).reset_index()[:10]
    print(Widowed['Profession'])
    values =  Widowed['Profession'].values
    top10Widowed[i]= values

top10Widowed = top10Widowed.reindex(sorted(top10Divorced.columns), axis=1)

top10Widowed.values[0]




