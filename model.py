import numpy as np
import numpy_financial as npf
import pandas as pd

def eligibility_check(df_finance):
    legiblestock = True
    reasons = []

    # EPS increases over the year (consistent)
    for growth in df_finance.eps_growth:
        if growth < 0:
            legiblestock = False
            reasons.append(f'there is negative growth: {growth:.4f}')
            break
    # ROE > 0.15
    if df_finance.roe.mean() < 0.13:
        legiblestock = False
        reasons.append(f'roe mean is less than 0.13: {df_finance.roe.mean():.4f}')
    # ROA > 0.07 (also consider debt to equity cause Assets = liabilities + equity)
    if df_finance.roa.mean() < 0.07:
        legiblestock = False
        reasons.append(f'roa mean is less than 0.07: {df_finance.roa.mean():.4f}')
    # Long term debt < 5 * income
    long_term_debt = df_finance.long_term_debt.tail(1).values[0]
    net_income = df_finance.net_income.tail(1).values[0]
    if long_term_debt > 5 * net_income:
        legiblestock = False
        reasons.append(f'long_term_debt is more than 5 times the net_income: {long_term_debt / net_income:.3f}')
    # Interest Coverage Ratio > 3
    interest_coverage = df_finance.interest_coverage.tail(1).values[0]
    if interest_coverage < 3:
        legiblestock = False
        reasons.append(f'interest_coverage is less than 3: {interest_coverage:.3f}')
    return reasons

def get_processed_price(df_price_raw):
    df_price_raw['year'] = df_price_raw.index.strftime('%Y')
    df_price_raw['month'] = df_price_raw.index.strftime('%m')
    df_price_raw.describe()
    df_price_raw = df_price_raw[df_price_raw['month']=='12']
    df_price = group_df(df_price_raw, ['year'], {'Close':['mean','std']})
    df_price.index = df_price['year']
    df_price = df_price.drop('year', axis=1).rename(columns={'Close_mean':'Close'})
    return df_price

def get_eps_growth(cur_eps, prev_eps):
    growth = 0
    if prev_eps >= 0 :
        growth = cur_eps/prev_eps - 1
    else:
        growth = 1 - cur_eps/prev_eps
    growth = min(growth, 5.0)
    growth = max(growth, -5.0)
    return growth

def get_processed_finance(df_finance_raw):
    df_finance = df_finance_raw
    df_finance['eps_growth'] = df_finance['eps'].pct_change()
    df_finance['roa'] = df_finance['net_income']/df_finance['total_asset']
    df_finance['roe'] = df_finance['net_income']/df_finance['holder_equity']
    df_finance['interest_coverage'] = df_finance['ebitda']/df_finance['interest_expense']
    return get_processed_finance

def get_effective_pe(df_price, df_finance):
    df_price = get_processed_price(df_price)
    df_merge = pd.merge(df_price, df_finance, left_index=True, right_index=True, how='inner')
    df_merge['pe_rat'] = df_merge['Close'] / df_merge['eps']
    return df_merge['pe_rat'].median()


def get_pred_price_df(ticker, df_finance, df_price, discount_rate, margin_rate, years=5):
    df_pred = pd.DataFrame(columns=['ticker', 'annual_growth', 'last_eps', 'future_eps'])

    try:
        annual_growth = npf.rate(len(df_finance), 0, -1 * df_finance.eps.iloc[0], df_finance.eps.tail(1).values[0])
        last_eps = df_finance.eps.tail(2).mean()
        future_eps = abs(npf.fv(annual_growth, years, 0, last_eps))
        df_pred.loc[0] = [ticker, annual_growth, last_eps, future_eps]
    except:
        print('eps does not exist')

    df_pred = df_pred.set_index('ticker')
    df_pred['pe_rat'] = get_effective_pe(df_price, df_finance)
    df_pred['fv'] = df_pred['future_eps'] * df_pred['pe_rat']
    df_pred['pv'] = abs(npf.pv(discount_rate, years, 0, fv=df_pred['fv']))
    if df_pred['fv'].values[0] > 0:
        df_pred['margin_price'] = df_pred['pv'] * (1 - margin_rate)
    else:
        df_pred['margin_price'] = 0

    df_pred['last_share_price'] = df_price.Close.tail(1).values[0]
    df_pred['decision'] = np.where((df_pred['last_share_price'] < df_pred['margin_price']), 'BUY', 'SELL')
    return df_pred


def group_df(df, group_column, agg_func):
    temp_df = df.groupby(group_column).agg(agg_func)
    temp_df.columns = ['_'.join(col) for col in temp_df.columns.values]
    temp_df.reset_index(inplace=True)
    return temp_df
