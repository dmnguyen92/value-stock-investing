import pandas as pd
import yfinance as yf
import numpy as np
import numpy_financial as npf

def get_financial_report(ticker):
    data = yf.Ticker(ticker)
    finance = data.financials.transpose()
    for col in ['Interest Expense', 'Basic EPS', 'Net Income']:
        if col not in finance.columns:
            finance[col] = 0.01
    df_finance_raw = finance[['Basic EPS', 'Net Income', 'Interest Expense', 'EBITDA']].fillna(0.01)

    balance = data.balance_sheet.transpose()
    for col in ['Long Term Debt', 'Basic EPS']:
        if col not in balance.columns:
            balance[col] = 0.01
    df_balance = balance[['Stockholders Equity', 'Long Term Debt', 'Total Assets']]

    df_finance = pd.concat([df_finance_raw, df_balance], axis=1)
    df_finance = df_finance.apply(pd.to_numeric, errors='coerce')
    df_finance = df_finance.set_axis(['eps', 'net_income', 'interest_expense', 'ebitda', 'holder_equity', 'long_term_debt', 'total_asset'], axis=1)
    df_finance = df_finance.sort_index()
    df_finance['eps_growth'] = df_finance['eps'].pct_change()
    df_finance['roa'] = df_finance['net_income']/df_finance['total_asset']
    df_finance['roe'] = df_finance['net_income']/df_finance['holder_equity']
    df_finance['interest_coverage'] = df_finance['ebitda']/df_finance['interest_expense']
    df_finance.index = pd.to_datetime(df_finance.index)
    df_finance.index = df_finance.index.year

    df_price = data.history(period='5y',interval='1mo')

    return df_price, df_finance
