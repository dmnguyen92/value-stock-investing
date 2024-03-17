import pandas as pd
import yfinance as yf
import numpy as np
import numpy_financial as npf
import datetime

# ticker= 'SE'

def get_financial_report_yahoo(ticker, years=10):
    data = yf.Ticker(ticker)
    finance = data.financials.transpose()
    for col in ['Interest Expense', 'Basic EPS', 'Net Income']:
        if col not in finance.columns:
            finance[col] = 0.01
    df_finance_raw = finance[['Basic EPS', 'Net Income', 'Interest Expense', 'EBITDA']]
    df_finance_raw = df_finance_raw.fillna(df_finance_raw.shift(-1))

    balance = data.balance_sheet.transpose()
    for col in ['Long Term Debt', 'Basic EPS']:
        if col not in balance.columns:
            balance[col] = 0.01
    df_balance = balance[['Stockholders Equity', 'Long Term Debt', 'Total Assets']]

    df_finance = pd.concat([df_finance_raw, df_balance], axis=1)
    df_finance = df_finance.apply(pd.to_numeric, errors='coerce')
    df_finance = df_finance.set_axis(['eps', 'net_income', 'interest_expense', 'ebitda', 'holder_equity', 'long_term_debt', 'total_asset'], axis=1)
    df_finance = df_finance.sort_index()
    df_finance.index = pd.to_datetime(df_finance.index)
    df_finance.index = df_finance.index.year

    cur_year = datetime.now().year
    cutoff_year = cur_year - years - 1
    df_finance.index = df_finance.index.year
    df_finance.index.name = "year"
    df_finance = df_finance[df_finance.index >= cutoff_year]

    return df_finance

def get_price_yahoo(ticker, years=10):
    data = yf.Ticker(ticker)
    df_price_raw = data.history(period=f'{years}y',interval='1d')
    return df_price_raw
