
#USE pandas and numpy packages
import pandas as pd
import numpy as np
import math
from pandas import Series, DataFrame, Panel
from pandas import read_csv

################################# Part(1) ########################################################

#Read Data
Data = pd.read_csv('spx.csv',  header=None,  names=['date', 'value'], index_col='date', parse_dates=['date'])
print Data


#Drop NA values
Data = Data.dropna()


#Resample Values to get the last-day value of each month
monthlyLastDayData = Data.resample('M', how='last')

#Resample Values to get the first-day value of each month
monthlyFirstDayData = Data.resample('M', how='first')


#Merge Data into the same dataFrame
MergedData = pd.merge(monthlyFirstDayData, monthlyLastDayData, left_index=True, right_index=True, how='outer')
MergedData.columns = ['FirstDayValue', 'LastDayValue']

#Calculate monthly return
MergedData['MonthlyReturn'] = MergedData.apply(lambda row: (row['LastDayValue'] - row['FirstDayValue'])*100 / row['FirstDayValue'],axis=1)

#Sort results by monthly return
SortedMonthlyData = MergedData.sort('MonthlyReturn', ascending=False)

##Part(1) Answer
# Print 3 best monthly returns
print SortedMonthlyData.head(3)
# Print 3 worst monthly returns
print SortedMonthlyData.tail(3)

################################# Part(2) ########################################################

#Assign month index 1 to 12  to each month
MergedData['monthIndex'] = MergedData.index.month


#Group by MonthIndex to calculate the average month return
DataGroupedByMonth = MergedData.groupby('monthIndex').mean()['MonthlyReturn']

##Part(2) Answer
#Print the the average month return  for each month
# We find December has the highest average return (1.756314%) and winter usually has the high average return
print DataGroupedByMonth


################################# Part(3) ########################################################

#create DataGroupByYear
DataGroupByYear = MergedData
#remove 'FirstDayValue', 'LastDayValue' and 'monthIndex'
DataGroupByYear = DataGroupByYear.drop(['FirstDayValue', 'LastDayValue','monthIndex'],axis=1)

#update monthlyReturn  to be  1 + monthlyReturn
DataGroupByYear['MonthlyReturn'] = DataGroupByYear.apply(lambda row: (row['MonthlyReturn'] + 100)/100,axis=1)
DataGroupByYear = DataGroupByYear.groupby(DataGroupByYear.index.year).cumprod()

#Resample Values to get the December-value  of each month
DataGroupByYear = DataGroupByYear.resample('A', how='last')

#decrement monthlyReturn  to be monthlyReturn -1
DataGroupByYear['MonthlyReturn'] = DataGroupByYear.apply(lambda row: (row['MonthlyReturn'] - 1)*100,axis=1)

#Rename monthlyReturn to be annualReturn
DataGroupByYear.columns = ['annualReturn']

#Print the  annual Return
print DataGroupByYear


################################# Part(4) ########################################################


#Define autorrealtion function
def acf(x):
    n = len(x)
    variance = x.var()
    x = x-x.mean()
    r = np.correlate(x, x, mode = 'full')[-n:]
    assert np.allclose(r, np.array([(x[:n-k]*x[-(n-k):]).sum() for k in range(n)]))
    result = r/(variance*(np.arange(n, 0, -1)))
    return result


#calculate the daily returns
dailyReturnData = []
for i in range(len(Data['value'])) :
   if(i >= 1):
       dailyReturnData.append((Data['value'][i] - Data['value'][i-1])*100 / Data['value'][i-1])

dailyReturnData = np.array(dailyReturnData)


##Part (4) Answer
#calculate the autocorrelation of daily returns at lag 1
autoCorr = acf(dailyReturnData)

print autoCorr

#calculate standard error at lag1
# approximately sqrt(1/ N)  where N is size of the series

sd = math.sqrt(1/len(Data['value']))
print sd