import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define your portfolio
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
weights = np.array([0.25, 0.25, 0.25, 0.25])  # Equal weighting

# Download historical adjusted closing prices
start_date = '2020-01-01'
end_date = '2024-01-01'
prices = yf.download(tickers, start=start_date, end=end_date)['Close']

# Compute daily returns
daily_returns = prices.pct_change().dropna()

# Calculate mean return and volatility of the portfolio
portfolio_returns = daily_returns.dot(weights)
mean_return = portfolio_returns.mean()
volatility = portfolio_returns.std()

# Simulate 1000 Monte Carlo paths
np.random.seed(42)
n_simulations = 1000
n_days = 252
initial_value = 100000
simulated_paths = np.zeros((n_days, n_simulations))

for i in range(n_simulations):
    simulated_returns = np.random.normal(mean_return, volatility, n_days)
    simulated_paths[:, i] = initial_value * np.cumprod(1 + simulated_returns)

# Compute max drawdown for each path
peak = np.maximum.accumulate(simulated_paths, axis=0)
drawdowns = (simulated_paths - peak) / peak
max_drawdowns = drawdowns.min(axis=0)

# Plot drawdown distribution
plt.figure(figsize=(10, 6))
plt.hist(max_drawdowns, bins=50, edgecolor='black')
plt.title('Simulated Maximum Drawdown Distribution')
plt.xlabel('Max Drawdown')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.show()
