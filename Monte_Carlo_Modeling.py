import pandas as pd
import numpy as np
from numpy import random as rn
import seaborn as sns

rn.seed(7)



Simulations = 50000
a = np.arange(1,Simulations+1)
df3 = pd.DataFrame(data=a)
df3['RAND'] = rn.rand(Simulations,1)
df3.drop([0], axis=1, inplace=True)

LowUsage = [0, 200, 1000]

df3['LowUsage'] = rn.triangular(*LowUsage, size=Simulations)

df3.mean()

PricePerUser = (df3['LowUsage'].mean()) * (0.0000015)

PricePerUser

Simulations = 50000
f = np.arange(1,Simulations+1)
df = pd.DataFrame(data=f)
df['RAND'] = rn.rand(Simulations,1)
df.drop([0], axis=1, inplace=True)

LowUsage = [0, 25, 75]
ModestUsage = [0, 25, 100]
HighUsage = [0, 50, 150]
VeryHighUsage = [0, 75, 200]
VeryVeryHighUsage = [10, 100, 200]

# Run Monte Carlo simulation for each distribution
df['LowUsage'] = rn.triangular(*LowUsage, size=Simulations)
df['ModestUsage'] = rn.triangular(*ModestUsage, size=Simulations)
df['HighUsage'] = rn.triangular(*HighUsage, size=Simulations)
df['VeryHighUsage'] = rn.triangular(*VeryHighUsage, size=Simulations)
df['VeryVeryHighUsage'] = rn.triangular(*VeryVeryHighUsage, size=Simulations)


# Low Low, Parameter estimates for each user distribution (question prompts)
ParamEstimates = df[['LowUsage', 'ModestUsage', 'HighUsage', 'VeryHighUsage', 'VeryVeryHighUsage']]

ParamEstimates

#Getting Prices Per User Per Distirubtion
PricesEstimatesInputPrices = ParamEstimates * 0.0006
PricesEstimatesOutputPrices = ParamEstimates * 0.002

PricesEstimatesInputPrices.mean()

PricesEstimatesOutputPrices

#Getting Visualizations for each parameter estimate
sns.histplot(df['LowUsage']).set(title = 'Low User Distirubtion Parameter Estimates')

#now we have data frames with price estimates, with this we will no do an estimation of initial educator class sizes
dfPricesInput = df[['LowUsage', 'ModestUsage', 'HighUsage', 'VeryHighUsage', 'VeryVeryHighUsage']] * 0.0006
dfPricesOutput =  df[['LowUsage', 'ModestUsage', 'HighUsage', 'VeryHighUsage', 'VeryVeryHighUsage']] * 0.002


#now lets estimate class room sizes with a similar framework
Simulations = 50000
r = np.arange(1,Simulations+1)
df1 = pd.DataFrame(data=r)
df1['RAND'] = rn.rand(Simulations,1)
df1.drop([0], axis=1, inplace=True)


ClassSizeDistribtuion = [20, 30, 50]

# Run Monte Carlo simulation for each distribution
df1['ClassSize'] = rn.triangular(*ClassSizeDistribtuion, size=Simulations)

df1.mean()


# Price Estimating Distributions (Average Per Class Cost, Per User)
dfCostInputMonth = df1['ClassSize'].mean() * PricesEstimatesInputPrices * 4
dfCostOutputMonth = df1['ClassSize'].mean() * PricesEstimatesOutputPrices * 4

dfCostInputYear = (df1['ClassSize'].mean() * PricesEstimatesInputPrices * 4) * 12
dfCostOutputYear = (df1['ClassSize'].mean() * PricesEstimatesOutputPrices * 4) * 12


#we now have average costs across each in each scenario for both inputs (questions) and output (generative texts)
#on a weekly basis, monthly basis
dfCostInputYear.mean()

dfCostOutputYear.mean()

#now we need to make assumptions around our growth rate
#assume we have n=100 (100 users), at this rate to break even assuing modest usage
#costs

def TokenCost(InputAvgCostYear, OutputAvgCostYear, Users):
    Cost = (InputAvgCostYear * Users) + (OutputAvgCostYear * Users)
    return Cost

def SubscriptionPrice(InputAvgCostYear, OutputAvgCostYear, Users):
    Cost = (InputAvgCostYear) + (OutputAvgCostYear * Users)
    AvgYearlyUserCost = Cost / Users
    Subscription = AvgYearlyUserCost / 12
    return np.round(Subscription,2)

#low end Subscription price
SubscriptionPrice(80, 106, 1)

#modest end subscription price
SubscriptionPrice(100, 133, 1)

#high usage price
SubscriptionPrice(160, 214, 1)

#very high usage
SubscriptionPrice(220, 293, 1)

#very very high usage
SubscriptionPrice(248, 331, 1)

#Depending on our assumptions on pricing distributions we can expect price to lie between
# [15.5 , 48.25]
#but our average is with very biased distributions, in reality we can excpect it to lie within [low,modest]
avgSubPrice = ((15.5 + 19.42 + 31.17 + 42.75 + 48.25) / 5)
print(avgSubPrice)


#now we need to run MC on opne AI embeddings
ParamEstimates.mean()

EmbeddingCostPerUser = ParamEstimates * 0.0001

YearlyEmbeddingCostPerUser = (((EmbeddingCostPerUser) * 12) * 30)

YearlyEmbeddingCostPerUser.mean()

def Subscription(InputAvgCostYear, OutputAvgCostYear, EmbeddingCostUser, Users):
    FixedCost = 740
    VariableCost = (InputAvgCostYear * Users) + (OutputAvgCostYear * Users) + (EmbeddingCostUser * Users)
    Cost = VariableCost + FixedCost
    AvgYearlyUserCost = Cost / Users
    Subscription = (AvgYearlyUserCost / 12)
    return np.round(Subscription,2), Cost

def FixedCost():
    Storage = 70 * 12
    return Sto

VariableCost = Subscription(80, 106, 1.2, 1)

#assuming very high use case we reommend a price of around 15 to attract a high user base, as our product scales, cost will decrease significantly
Subscription(32, 106, 1.2, 100)
