import yfinance as yf
import pandas as pd

# Define 50 tickers per sector
sectors = {
    'Technology': [
        'AAPL', 'MSFT', 'NVDA', 'ADBE', 'CRM', 'CSCO', 'ORCL', 'INTC', 'AMD', 'QCOM',
        'IBM', 'TXN', 'AVGO', 'MU', 'HPQ', 'DELL', 'WDAY', 'ZM', 'SNOW', 'NOW',
        'SAP', 'UBER', 'SHOP', 'PYPL', 'TWLO', 'DOCU', 'FSLY', 'NET', 'CRWD',
        'PANW', 'ZS', 'OKTA', 'TEAM', 'MDB', 'ESTC', 'DDOG', 'PLTR', 'ASAN',
        'MNDY', 'BOX', 'ANSS', 'CDNS', 'SNPS', 'AKAM', 'CHKP', 'FTNT', 'CYBR'
    ],
    'Healthcare': [
        'JNJ', 'PFE', 'MRK', 'ABBV', 'LLY', 'TMO', 'BMY', 'GILD', 'CVS', 'UNH',
        'AMGN', 'BIIB', 'REGN', 'VRTX', 'MDT', 'ISRG', 'SYK', 'BDX', 'ZBH', 'HCA',
        'CNC', 'CI', 'HUM', 'MOH', 'ELV', 'MCK', 'CAH', 'DGX', 'LH',
        'IQV', 'MTD', 'WST', 'STE', 'HSIC', 'XRAY', 'ALGN', 'HOLX', 'IDXX', 'BIO',
        'TECH', 'QGEN', 'RGEN', 'BAX', 'BHC', 'UHS', 'PINC', 'OPCH', 'AMED', 'EHC'
    ],
    'Financials': [
        'JPM', 'BAC', 'WFC', 'GS', 'MS', 'AXP', 'C', 'BLK', 'SCHW', 'SPGI',
        'USB', 'PNC', 'TFC', 'BK', 'STT', 'AIG', 'PRU', 'MET', 'ALL', 'TRV',
        'CB', 'CINF', 'PGR', 'LNC', 'UNM', 'AFL', 'HIG', 'CMA', 'RF', 'FITB',
        'KEY', 'MTB', 'HBAN', 'ZION', 'CFG', 'ALLY', 'NTRS', 'BEN', 'TROW',
        'AMP', 'LPLA', 'IVZ', 'EVR', 'PJT', 'MC', 'LAZ', 'BKD', 'FDS'
    ],
    'Industrials': [
        'BA', 'HON', 'UPS', 'CAT', 'DE', 'LMT', 'MMM', 'GE', 'NOC', 'RTX',
        'GD', 'EMR', 'ETN', 'PCAR', 'FAST', 'FLS', 'IR', 'JCI', 'PH', 'ROK',
        'DOV', 'XYL', 'AOS', 'PNR', 'ITW', 'SWK', 'SNA', 'CMI', 'DHR', 'FMC',
        'GWW', 'IEX', 'LECO', 'MAS', 'PNW', 'PWR', 'RSG', 'VMC', 'WAB', 'WM',
        'WTS', 'XYL', 'CSX', 'NSC', 'UNP', 'JBHT', 'ODFL', 'CHRW', 'EXP', 'MLM'
    ],
    'Consumer Discretionary': [
        'AMZN', 'TSLA', 'HD', 'MCD', 'SBUX', 'LOW', 'NKE', 'BKNG', 'TGT', 'ROST',
        'TJX', 'MAR', 'HLT', 'YUM', 'DG', 'F', 'GM', 'EBAY', 'ULTA', 'LULU',
        'ORLY', 'AZO', 'AAP', 'BBY', 'KSS', 'JWN', 'M',
        'HAS', 'MAT', 'LEG', 'WHR', 'POOL', 'WSM', 'RH', 'TPR', 'VFC', 'PVH',
        'RL', 'HBI', 'CROX', 'DECK', 'SKX', 'COLM', 'GIL', 'LEVI', 'MOV', 'SHOO'
    ]
}

# Flatten tickers list
tickers = [ticker for tickers_in_sector in sectors.values() for ticker in tickers_in_sector]

# Download Adjusted Close price data
data = yf.download(tickers, start="2010-01-01", end="2023-12-31", interval="1d", auto_adjust=False)['Adj Close']

# Save sector mapping
sector_map = {ticker: sector for sector, tickers_in_sector in sectors.items() for ticker in tickers_in_sector}
pd.Series(sector_map, name='Sector').to_csv('sector_mapping.csv')

# Save Adjusted Close price data
data.to_csv('adjusted_close_prices.csv')

print("Data Downloaded and Saved Successfully")
