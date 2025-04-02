import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np


# What are your goals and restrictions for the model?
goal = 'maxProfit'
maxCompanies = 20
exposureLimit = 0.33
minInvestment = 0.01
maxInvestment = 0.33
maxRisk = 0.01


# Read the data
prices = pd.read_csv('adjusted_close_prices.csv', index_col=0).dropna()  # first column is "dates"
companySectors = pd.read_csv('sector_mapping.csv', header=None, names=['Company', 'Sector'])
numDays = prices.shape[0]
numCompanies = prices.shape[1]
sectors = companySectors.iloc[:, 1].unique()
numSectors = len(sectors)
companySectorMap = dict(zip(companySectors['Company'], companySectors['Sector']))


# Compute Log Returns of Stocks
returns = np.zeros((numDays - 1, numCompanies))
for i in range(numDays - 1):                # first row is the name of the company
    for t in range(numCompanies):           # we are calculating differences, so start one day forward
        returns[i, t] = np.log(prices.iloc[i + 1, t] / prices.iloc[i, t])


# Compute the Mean Return Vector
mu = np.zeros(numCompanies)
for i in range(numCompanies):
    mu[i] = np.mean(returns[:, i])


# Compute the covariance matrix
sigma = 1 / (numDays - 2) * np.dot((returns - mu).T, (returns - mu))  # we do -2 since we have one less day now


# Set the model parameters
R = np.mean(mu)                                      # target return (historical average of the assets)
K = maxCompanies                                     # cardinality limit (max number of companies in portfolio)
s = {sector: exposureLimit for sector in sectors}    # sector exposure limit
l = {i: minInvestment for i in range(numCompanies)}  # minimum investment per selected asset
m = {i: maxInvestment for i in range(numCompanies)}  # maximum investment per selected asset 


# Initialize the Gurobi model
model = gp.Model("Portfolio Maximization")


# Set the model decision variables
x = model.addVars(numCompanies, lb=0, name='x')
y = model.addVars(numCompanies, vtype=GRB.BINARY, name='y')


# Determine our objective function
if goal == 'maxProfit':
    # Set the model objective: maximize return
    model.setObjective(
        gp.quicksum(mu[i] * x[i] for i in range(numCompanies)),
        GRB.MAXIMIZE
    )
else:
    # Set the model objective: minimize portfolio variance
    model.setObjective(
        gp.quicksum(x[i] * sigma[i, j] * x[j] for i in range(numCompanies) for j in range(numCompanies)), 
        GRB.MINIMIZE
    )


# Add the constraints for each asset
for i in range(numCompanies):
    model.addConstr(x[i] <= m[i] * y[i])  # maximum investment per asset
    model.addConstr(x[i] >= l[i] * y[i])  # minimum investment per asset
    model.addConstr(x[i] <= y[i])
    
if goal == 'maxProfit':
    model.addConstr(gp.quicksum(x[i] * sigma[i, j] * x[j] for i in range(numCompanies) for j in range(numCompanies)) <= maxRisk ** 2)


model.addConstr(gp.quicksum(mu[i] * x[i] for i in range(numCompanies)) >= R)    # Target return constraint
model.addConstr(gp.quicksum(x[i] for i in range(numCompanies)) == 1)            # Budget constraint: total allocation sums to 1
model.addConstr(gp.quicksum(y[i] for i in range(numCompanies)) <= K)            # Cardinality constraint: maximum number of selected assets

# Sector exposure constraints:
# For each sector, sum the investments of companies belonging to that sector and ensure it does not exceed the limit.
for sector in sectors:
    model.addConstr(
        gp.quicksum(x[i] for i in range(numCompanies) 
                    if companySectorMap[prices.columns[i]] == sector) <= s[sector]
    )


# Optimize the model
model.optimize()


# Extract and display results
if model.status == GRB.OPTIMAL:
    print("\nOptimal solution found!\n")

    selectedCompanies = []
    weights = []

    # Gather the selected companies (where y[i] > 0.5) and their corresponding weights
    for i in range(numCompanies):
        if y[i].x > 0.5:
            selectedCompanies.append(prices.columns[i])
            weights.append(x[i].x)

    print("Selected Companies & Allocations:")
    for company, weight in zip(selectedCompanies, weights):
        sector = companySectorMap[company]
        print(f"{company} ({sector}): {weight:.4f}")

    # Portfolio metrics
    portfolioReturn = sum(mu[i] * x[i].x for i in range(numCompanies))  # Daily expected return
    portfolioVariance = sum(x[i].x * sigma[i, j] * x[j].x
                            for i in range(numCompanies)
                            for j in range(numCompanies))              # Daily variance
    portfolioRisk = np.sqrt(portfolioVariance)                         # Daily standard deviation

    # Annualized metrics
    annualizedReturn = portfolioReturn * 252                           # Annualized expected return
    annualizedRisk = portfolioRisk * np.sqrt(252)                      # Annualized standard deviation

    print(f"\nPortfolio Expected Daily Return: {portfolioReturn * 100:.4f}%")
    print(f"Portfolio Expected Annualized Return: {annualizedReturn * 100:.2f}%")
    print(f"Portfolio Daily Risk (Std Dev): {portfolioRisk * 100:.4f}%")
    print(f"Portfolio Annualized Risk (Std Dev): {annualizedRisk * 100:.2f}%")

    # Sector exposure calculation
    sectorExposure = {sector: 0.0 for sector in sectors}
    for i in range(numCompanies):
        company = prices.columns[i]
        sector = companySectorMap[company]
        sectorExposure[sector] += x[i].x

    print("\nSector Exposure:")
    for sector, exposure in sectorExposure.items():
        print(f"{sector}: {exposure:.4f}")

else:
    print("\nNo optimal solution found. Status code:", model.status)

