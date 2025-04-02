# 💰 Quadratic Portfolio Optimization Using Gurobi

This project formulates and solves a **constrained portfolio optimization problem** using **Mixed-Integer Quadratic Programming (MIQP)** in Python with **Gurobi**.  
The goal is to construct an optimal portfolio by either:
- **Maximizing expected return** under a risk constraint  
**or**
- **Minimizing portfolio risk** while achieving a minimum expected return

It includes realistic financial constraints:
- **Cardinality limit**
- **Sector exposure limits**
- **Minimum and maximum investment per asset**

---

## 🧩 Model Formulation

### Objective Functions

Depending on the selected goal (`maxProfit` or `minRisk`), the model solves one of the following:

**Maximize expected return:**
$$
\max \sum_{i=1}^N \mu_i x_i
$$
subject to a risk constraint:
$$
x^T \Sigma x \leq \text{{maxRisk}}^2
$$

**Minimize risk (variance):**
$$
\min x^T \Sigma x
$$

---

### Constraints
For both objectives, the following constraints are applied:

**Budget constraint:**
$$
\sum_{i=1}^N x_i = 1
$$

**Target return constraint (only for risk minimization):**
$$
\sum_{i=1}^N \mu_i x_i \geq R
$$

**Cardinality constraint (max number of selected assets):**
$$
\sum_{i=1}^N y_i \leq K
$$

**Sector exposure constraints:**
For each sector \( s \):
$$
\sum_{i \in s} x_i \leq s_{\text{limit}}
$$

**Investment bounds per asset:**
$$
l_i y_i \leq x_i \leq m_i y_i
$$

**Binary selection variables:**
$$
y_i \in \{0, 1\}
$$

---

## ⚙️ Parameters & Customization

You can easily modify model parameters in `model.py`:

```python
goal = 'maxProfit'            # Choose 'maxProfit' or 'minRisk'
maxCompanies = 20             # Max number of companies in the portfolio
exposureLimit = 0.33          # Max sector exposure
minInvestment = 0.01          # Min investment per selected company
maxInvestment = 0.33          # Max investment per selected company
maxRisk = 0.01                # Risk constraint (only applies to maxProfit objective)
```

---

## 📁 Files

| File                  | Description                                             |
|----------------------:|:-------------------------------------------------------:|
| `model.py`            | Full implementation of the MIQP portfolio optimization model |
| `adjusted_close_prices.csv` | Daily adjusted closing price data for selected stocks |
| `sector_mapping.csv`  | Mapping of company tickers to sectors                   |
| `stockInfo.py`        | Optional script for pre-processing or downloading data  |

---

## 📊 Outputs

After solving, the model will display:

- ✅ **Selected companies and their weights**
- ✅ **Portfolio expected daily return and annualized return**
- ✅ **Portfolio daily and annualized risk (standard deviation)**
- ✅ **Sector exposure breakdown**
- ❗️ Message if no feasible solution is found

Example Output:

```
Optimal solution found!

Selected Companies & Allocations:
AAPL (Technology): 0.3300
LLY (Healthcare): 0.3300
PWR (Industrials): 0.3300
DECK (Consumer Discretionary): 0.0100

Portfolio Expected Daily Return: 0.0015%
Portfolio Expected Annualized Return: 37.80%
Portfolio Daily Risk (Std Dev): 1.80%
Portfolio Annualized Risk (Std Dev): 28.56%

Sector Exposure:
Technology: 0.3300
Healthcare: 0.3300
Industrials: 0.3300
Consumer Discretionary: 0.0100
Financials: 0.0000
```

---

## 📥 How to Change Company Universe

You can easily change the set of companies and sectors used in the model by modifying and running the `stockInfo.py` script.  
Example snippet:

```python
import yfinance as yf
import pandas as pd

# Define tickers per sector
sectors = {
    'Technology': [...],
    'Healthcare': [...],
    'Financials': [...],
    'Industrials': [...],
    'Consumer Discretionary': [...]
}

# Download data
tickers = [ticker for tickers_in_sector in sectors.values() for ticker in tickers_in_sector]
data = yf.download(tickers, start="2010-01-01", end="2023-12-31", interval="1d")["Adj Close"]
data.to_csv("adjusted_close_prices.csv")

# Save sector mapping
sector_map = {ticker: sector for sector, tickers_in_sector in sectors.items() for ticker in tickers_in_sector}
pd.Series(sector_map, name='Sector').to_csv('sector_mapping.csv')
```

---

## 📦 Dependencies

- `gurobipy`
- `pandas`
- `numpy`
- `yfinance` (for optional data collection)

---

## 🔍 Purpose

This repository demonstrates a full end-to-end **realistic portfolio optimization workflow** including:
- Real financial data
- Hard practical constraints
- Quadratic programming formulation
